import typer
import asyncio
import os
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from typing import Optional, Dict, Tuple, Any
from functools import partial
from .ui.welcome import show_welcome_screen
from .ui.terminal import FridayTerminal
from .ui.loader import FridayLoader
from .core.engine import run_ai, MODEL_3_7
from .core.chat import (
    Sender,
    _render_message,
    _tool_output_callback,
    _api_response_callback,
)
from .core.tools import ToolResult

app = typer.Typer(
    name="FRIDAY AI CLI",
    help="Your AI-powered software development assistant",
    add_completion=False,
)

console = Console()

# Global state for storing responses and tool outputs
response_state: Dict[str, Tuple[httpx.Request, Any]] = {}
tool_state: Dict[str, ToolResult] = {}


async def start_chat_session(api_key: Optional[str] = None):
    """Initialize and start the chat session"""
    messages = []

    # Get API key from environment or user input
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = typer.prompt("Enter your Anthropic API Key", hide_input=True)

    # Start the chat loop
    try:
        while True:
            # Add a newline for spacing
            console.print("")
            # Get user input with styled prompt
            user_input = typer.prompt("👤 You: ", prompt_suffix=" ›")
            # Add a newline for spacing
            console.print("")

            # Echo user input with proper formatting
            # console.print(
            #     Panel(
            #         Markdown(user_input),
            #         border_style="cyan",
            #         title="👤 [User]",
            #         title_align="left",
            #         padding=(1, 2),
            #     )
            # )
            if user_input.lower() in {"exit", "quit"}:
                console.print("\n[yellow]Goodbye! Have a great day! 👋[/yellow]")
                break

            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})
            try:
                # Run the sampling loop
                messages = await run_ai(
                    system_prompt_suffix="",
                    messages=messages,
                    output_callback=partial(_render_message, Sender.BOT),
                    tool_output_callback=partial(
                        _tool_output_callback, tool_state=tool_state
                    ),
                    api_response_callback=partial(
                        _api_response_callback, response_state=response_state
                    ),
                    api_key=api_key,
                    model=MODEL_3_7,
                    token_efficient_tools_beta=True,
                )
            except Exception as e:
                console.print(f"\n[red]Error during message processing: {str(e)}[/red]")
                if hasattr(e, "response"):
                    console.print(
                        f"[red]Response status: {e.response.status_code}[/red]"
                    )
                    console.print(f"[red]Response body: {e.response.text}[/red]")
                raise
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye! Have a great day! 👋[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {str(e)}[/red]")


@app.command()
def chat(
    api_key: str = typer.Option(None, "--api-key", "-k", help="Anthropic API Key"),
    model: str = typer.Option(MODEL_3_7, "--model", "-m", help="Claude model to use"),
):
    """Start a chat session with FRIDAY"""
    show_welcome_screen()
    asyncio.run(start_chat_session(api_key))


@app.command()
def version():
    """Show FRIDAY AI CLI version"""
    console.print("[cyan]FRIDAY AI CLI[/cyan] [green]v0.1.0[/green]")
    console.print(
        f"\n[white]Using Claude Model:[/white] [magenta]{MODEL_3_7}[/magenta]"
    )
    console.print("[white]Developed by:[/white] [yellow]Yash[/yellow]")


if __name__ == "__main__":
    app()
