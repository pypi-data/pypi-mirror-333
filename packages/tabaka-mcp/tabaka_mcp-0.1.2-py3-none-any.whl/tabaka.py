import asyncio
from dataclasses import dataclass
import multiprocessing
import multiprocessing.pool
from typing import Any, Optional, AsyncIterator
import signal
import docker
from docker.models.containers import Container
import httpx
import typer
from typer import Typer
import subprocess
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context
from mcp import types
from rich import print
from contextlib import asynccontextmanager

from pydantic import BaseModel, Field

from mcp.server.fastmcp.utilities.types import Image

from tabaka_core import Tabaka, TabakaConfig


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict[str, Any]]:
    """Manage application lifecycle with type-safe context"""
    try:
        # Initialize on startup
        yield {
            "sandbox": Tabaka(config=TabakaConfig(allowed_languages=["python", "go"]))
        }
    except Exception as e:
        print(f"[red]Error: {e}[/red]")
        raise e


app = FastMCP(
    "tabaka",
    lifespan=app_lifespan,
    debug=True,
    uvicorn_config_timeout_graceful_shutdown=0,
)
cli = Typer(
    name="tabaka",
    help="Tabaka MCP Server CLI",
    add_completion=False,
    no_args_is_help=True,
)


# @app.tool()
# def tabaka_execute_code(
#     ctx: Context,
#     code: str = Field(..., description="The code to execute"),
#     language_id: str = Field(
#         "python",
#         description="Language to execute the code in, e.g. 'python', 'go', 'javascript', etc.",
#     ),
#     required_packages: list[str] = Field(
#         default_factory=list,
#         description="Packages to install before execution, non-standard library packages, e.g. 'requests', 'numpy', 'pandas', etc.",
#     ),
#     timeout: Optional[int] = Field(
#         180, description="Maximum execution time in seconds"
#     ),
# ) -> str:
#     sandbox: Tabaka = ctx.request_context.lifespan_context["sandbox"]
#     return sandbox.execute_code(
#         code, language_id, required_packages, timeout
#     ).model_dump_json()


@app.tool()
def tabaka_list_containers(ctx: Context) -> list[str]:
    sandbox: Tabaka = ctx.request_context.lifespan_context["sandbox"]
    return sandbox.list_containers()


@app.tool()
def tabaka_run_terminal_command(
    ctx: Context,
    command: str = Field(
        ...,
        description="The command to run, you can use it to install packages, save files, read files, list files, etc.",
    ),
    container_id: str = Field(
        ...,
        description="The container ID to use for execution",
    ),
) -> str:
    sandbox: Tabaka = ctx.request_context.lifespan_context["sandbox"]
    return sandbox.run_terminal_command(command, container_id)


@cli.command()
def start():
    """Start the Tabaka MCP server."""
    # Start the server as a detached process
    script_path = Path(__file__).resolve()
    cmd = [sys.executable, str(script_path), "run"]
    _proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    print("[green]Started the Tabaka server[/green]")


def run_app(mode: str):
    app.run(transport="stdio" if mode == "stdio" else "sse")


@cli.command()
def run(
    mode: str = Field(
        default="sse",
        description="The mode to run the server in, e.g. 'stdio' or 'sse'",
    )
):
    """Run the server in the foreground."""

    # TODO: Find a better way to handle this
    # See: https://github.com/encode/uvicorn/discussions/1103
    with multiprocessing.Pool(processes=1) as pool:
        try:
            pool.apply(func=run_app, args=(mode,))
            # app.run(transport="stdio" if mode == "stdio" else "sse")
        except KeyboardInterrupt:
            print("[yellow]Server interrupted by user.[/yellow]")
        except Exception as e:
            print(f"[red]Error: {e}[/red]")
        finally:
            try:
                pool.terminate()
                clean_containers()
            except Exception as e:
                print(f"[red]Error cleaning up Docker containers: {e}[/red]")

    exit(0)


@cli.command()
def stop():
    """Stop the Tabaka server and clean up any Docker containers."""
    print(
        "[yellow]Stopping Tabaka server and cleaning up Docker containers...[/yellow]"
    )

    # Find processes that match our server pattern
    server_stopped = False

    try:
        if sys.platform == "win32":
            # Windows approach
            subprocess.run(
                ["taskkill", "/F", "/FI", "WINDOWTITLE eq *tabaka*"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            server_stopped = True
        else:
            # Unix approach - find processes with "tabaka-mcp" in command line
            # More elegant solution using pkill
            result = subprocess.run(
                ["pkill", "-f", "tabaka"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            server_stopped = result.returncode == 0
    except Exception as e:
        print(f"[yellow]Note: Process termination attempt: {e}[/yellow]")

    # Clean up Docker containers
    clean_containers()

    if server_stopped:
        print("[green]Server processes stopped successfully.[/green]")
    else:
        print(
            "[yellow]No running server processes found or unable to stop them.[/yellow]"
        )


def clean_containers():
    """Clean up Docker containers related to Tabaka."""
    try:
        # Stop all containers at once
        docker_client = docker.from_env()
        should_print = False
        for container in docker_client.containers.list(all=True):
            container: Container = container
            if container.name.startswith("tabaka-"):
                should_print = True
                print(f"[yellow]Stopping container: {container.name}[/yellow]")
                container.stop(timeout=1)
        if should_print:
            print("[green]Docker containers cleaned up successfully.[/green]")
    except Exception as e:
        print(f"[red]Error cleaning up Docker containers: {e}[/red]")


if __name__ == "__main__":
    cli()
