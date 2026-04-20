#!/usr/bin/env python3
"""ZPI-WARPAI: Local CLI Agent for Warp UIX. Uses Ollama.

Environment Safety:
    This script self-validates that it is running inside the project's
    virtual environment (.venv). If invoked from a system Python or a
    different venv, it will automatically re-launch itself using the
    correct interpreter. This guarantees all pinned dependencies
    (ollama, click, rich, aider-chat) resolve correctly every time.

References:
    - Python venv docs: https://docs.python.org/3/library/venv.html
    - sys.prefix vs sys.base_prefix: https://peps.python.org/pep-0405/
"""

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# STEP 0: Virtual-environment bootstrap (runs before any third-party import)
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / '.venv'

def _is_inside_project_venv() -> bool:
    """Return True only if the running interpreter is the project's .venv.

    We compare the resolved prefix against the project's .venv directory.
    This catches three failure modes:
        1. Running from bare system Python (sys.prefix == sys.base_prefix)
        2. Running from a *different* venv (e.g. .venv-1, conda, global)
        3. Running after the venv was recreated at a new path

    Reference: PEP 405 — https://peps.python.org/pep-0405/
    """
    if not VENV_DIR.exists():
        return False
    # Resolve both to handle symlinks / junction points on Windows
    current_prefix = Path(sys.prefix).resolve()
    expected_prefix = VENV_DIR.resolve()
    return current_prefix == expected_prefix


def _get_venv_python() -> Path:
    """Return the path to the venv's Python interpreter.

    On Windows the interpreter lives in Scripts/python.exe;
    on POSIX it lives in bin/python.

    Reference: https://docs.python.org/3/library/venv.html
    """
    if sys.platform == 'win32':
        return VENV_DIR / 'Scripts' / 'python.exe'
    return VENV_DIR / 'bin' / 'python'


def _get_venv_bin_dir() -> Path:
    """Return the venv's Scripts (Windows) or bin (POSIX) directory."""
    if sys.platform == 'win32':
        return VENV_DIR / 'Scripts'
    return VENV_DIR / 'bin'


def _bootstrap_venv() -> None:
    """Re-exec this script under the project venv if we aren't in it.

    This function never returns on success — it replaces the current
    process via subprocess (Windows) or os.execv (POSIX).
    """
    if _is_inside_project_venv():
        return  # Already correct — proceed normally

    venv_python = _get_venv_python()

    if not venv_python.exists():
        # Provide actionable error instead of a cryptic ImportError
        print(
            f"\n[ERROR] Project virtual environment not found at:\n"
            f"        {VENV_DIR}\n\n"
            f"  Run the installer first:\n"
            f"        .\\install.bat\n\n"
            f"  Or create it manually:\n"
            f"        python -m venv \"{VENV_DIR}\"\n"
            f"        \"{venv_python}\" -m pip install -r requirements.txt\n",
            file=sys.stderr,
        )
        sys.exit(1)

    # Re-launch under the correct interpreter, forwarding all CLI args.
    # On Windows os.execv can be unreliable with GUI Python, so we use
    # subprocess and propagate the exit code instead.
    import subprocess as _sp
    result = _sp.run([str(venv_python), __file__] + sys.argv[1:])
    sys.exit(result.returncode)


# --- Run the bootstrap BEFORE importing any third-party packages ---
_bootstrap_venv()

# ---------------------------------------------------------------------------
# Third-party imports (safe — we are guaranteed to be in .venv now)
# ---------------------------------------------------------------------------

import yaml          # pyyaml  — https://pypi.org/project/PyYAML/
import click         # click   — https://click.palletsprojects.com/
import ollama        # ollama  — https://pypi.org/project/ollama/
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.prompt import Prompt
import subprocess

console = Console()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config() -> dict:
    """Load config.yaml from the project directory."""
    config_path = BASE_DIR / 'config.yaml'
    if not config_path.exists():
        console.print(
            f"[bold red]Config not found:[/] {config_path}\n"
            f"Copy config.example.yaml → config.yaml and edit it.",
        )
        sys.exit(1)
    with open(config_path) as f:
        return yaml.safe_load(f)


def check_ollama_server(host: str) -> None:
    """Verify Ollama is reachable before making LLM calls.

    Sends a lightweight HTTP request to the Ollama health endpoint.
    Reference: https://github.com/ollama/ollama/blob/main/docs/api.md
    """
    import urllib.request
    import urllib.error
    try:
        urllib.request.urlopen(host, timeout=3)
    except (urllib.error.URLError, OSError):
        console.print(
            f"[bold red]Ollama server unreachable at {host}[/]\n"
            f"  Start it with: [cyan]ollama serve[/]\n"
            f"  Or check config.yaml → ollama_host",
        )
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@click.group()
@click.version_option()
@click.option('--model', default=None, help='Override the Ollama model for this session')
@click.pass_context
def cli(ctx, model):
    """ZPI-WARPAI — Local AI coding agent for Warp terminal."""
    config = load_config()
    if model:
        config['default_model'] = model

    host = config.get('ollama_host', 'http://localhost:11434')
    os.environ['OLLAMA_HOST'] = host

    if config.get('tor_proxy'):
        os.environ['HTTP_PROXY'] = config['tor_proxy']
        os.environ['HTTPS_PROXY'] = config['tor_proxy']

    # Store config on the Click context so subcommands can access it
    # without re-invoking the group (which caused double-execution).
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['host'] = host


@cli.command()
@click.argument('prompt', nargs=-1)
@click.pass_context
def chat(ctx, prompt):
    """Interactive chat with your local model."""
    config = ctx.obj['config']
    check_ollama_server(ctx.obj['host'])

    full_prompt = ' '.join(prompt)
    if not full_prompt:
        full_prompt = Prompt.ask('[bold cyan]Chat[/]')

    resp = ollama.chat(
        model=config['default_model'],
        messages=[{"role": "user", "content": full_prompt}],
    )
    console.print(Panel(Markdown(resp['message']['content']), title='WarpAI'))


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.pass_context
def review(ctx, file_path):
    """Code review a file with your local model."""
    config = ctx.obj['config']
    check_ollama_server(ctx.obj['host'])

    with open(file_path) as f:
        code = f.read()

    lang = Path(file_path).suffix[1:] or 'text'
    prompt = f"Review this {lang} code and suggest improvements:\n```\n{code}\n```"

    resp = ollama.chat(
        model=config['default_model'],
        messages=[{"role": "user", "content": prompt}],
    )
    console.print(Syntax(code, lang, theme='github-dark', line_numbers=True))
    console.print(Panel(Markdown(resp['message']['content']), title='Review'))


@cli.command()
@click.option('--task', required=True, help='Task description for the agent')
@click.option('--file', 'files', multiple=True, help='Files to include in context')
@click.pass_context
def agent(ctx, task, files):
    """Agent task completion (delegates to Aider when enabled)."""
    config = ctx.obj['config']
    check_ollama_server(ctx.obj['host'])

    if config.get('aider_enabled', True):
        # Resolve aider binary from THIS venv — not from system PATH.
        # This prevents running a stale or wrong aider installation.
        aider_bin = _get_venv_bin_dir() / ('aider.exe' if sys.platform == 'win32' else 'aider')

        if not aider_bin.exists():
            console.print(
                f"[bold red]Aider not found in venv:[/] {aider_bin}\n"
                f"  Install it: [cyan]{_get_venv_python()} -m pip install aider-chat[/]",
            )
            sys.exit(1)

        # Build command using the venv-local aider binary
        cmd = [
            str(aider_bin),
            '--model', f"ollama_chat/{config['default_model']}",
            '--message', task,
        ] + list(files)

        # Pass OLLAMA_API_BASE so Aider finds the local server
        env = os.environ.copy()
        env['OLLAMA_API_BASE'] = ctx.obj['host']

        console.print(f"[dim]→ Running:[/] {' '.join(cmd)}\n")
        subprocess.run(cmd, env=env)
    else:
        prompt = f"Complete task: {task}"
        if files:
            for f in files:
                with open(f) as ff:
                    prompt += f"\nFile {f}:\n```\n{ff.read()}\n```"
        resp = ollama.chat(
            model=config['default_model'],
            messages=[{"role": "user", "content": prompt}],
        )
        console.print(Panel(Markdown(resp['message']['content']), title='Agent Output'))


if __name__ == '__main__':
    cli()

