#!/usr/bin/env python3
\"\"\"ZPI-WARPAI: Local CLI Agent for Warp UIX. Uses Ollama.\"\"\"

import os
import sys
import yaml
import click
import ollama
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel
from rich.prompt import Prompt
from pathlib import Path
import subprocess

console = Console()
BASE_DIR = Path(__file__).parent

def load_config():
    config_path = BASE_DIR / 'config.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)

@click.group()
@click.version_option()
@click.option('--model', default=None, help='Ollama model')
def cli(model):
    config = load_config()
    if model:
        config['default_model'] = model
    os.environ['OLLAMA_HOST'] = config.get('ollama_host', 'http://localhost:11434')
    if config.get('tor_proxy'):
        os.environ['HTTP_PROXY'] = config['tor_proxy']
        os.environ['HTTPS_PROXY'] = config['tor_proxy']
    return config

@cli.command()
@click.argument('prompt', nargs=-1)
@click.pass_context
def chat(ctx, prompt):
    \"\"\"Interactive chat mode.\"\"\"
    config = ctx.invoke(cli)
    full_prompt = ' '.join(prompt)
    if not full_prompt:
        full_prompt = Prompt.ask('Chat')
    resp = ollama.chat(model=config['default_model'], messages=[
        {"role": "user", "content": full_prompt}
    ])
    console.print(Panel(Markdown(resp['message']['content']), title='WarpAI'))

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.pass_context
def review(ctx, file_path):
    \"\"\"Code review.\"\"\"
    config = ctx.invoke(cli)
    with open(file_path) as f:
        code = f.read()
    lang = Path(file_path).suffix[1:] or 'text'
    prompt = f"Review this {lang} code and suggest improvements:\n```\n{code}\n```"
    resp = ollama.chat(model=config['default_model'], messages=[
        {"role": "user", "content": prompt}
    ])
    console.print(Syntax(code, lang, theme='github-dark', line_numbers=True))
    console.print(Panel(Markdown(resp['message']['content']), title='Review'))

@cli.command()
@click.option('--task', required=True, help='Task description')
@click.option('--file', 'files', multiple=True, help='Files to edit')
@click.pass_context
def agent(ctx, task, files):
    \"\"\"Agent task completion (Aider-style).\"\"\"
    config = ctx.invoke(cli)
    prompt = f"Complete task: {task}"
    if files:
        for f in files:
            with open(f) as ff:
                prompt += f"\nFile {f}:\n```\n{ff.read()}\n```"
    if config.get('aider_enabled', True):
        cmd = ['aider', '--model', config['default_model'], '--message', task] + list(files)
        subprocess.run(cmd)
    else:
        resp = ollama.chat(model=config['default_model'], messages=[
            {"role": "user", "content": prompt}
        ])
        console.print(Panel(Markdown(resp['message']['content']), title='Agent Output'))

if __name__ == '__main__':
    cli()

