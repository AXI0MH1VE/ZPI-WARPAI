# ZPI-WARPAI: Local-Only WarpAI Agent

Warp provides deep UIX for agents, but free users can't fully replace paid backends with local models in native Agent Mode. **ZPI-WARPAI** is a custom CLI agent using Ollama for 100% local inference, designed to run inside Warp for full UIX (Agent Toolbelt, rich editor, interactive review) without subscriptions.

[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-brightgreen)](https://ollama.com/) [![Warp](https://img.shields.io/badge/Warp-UIX-blue)](https://warp.dev/)

## Features
- **Local-Only**: Llama3/Mistral via Ollama (no cloud/API keys).
- **Warp UIX**: Rich output, syntax highlight, multi-line prompts.
- **Modes**: `chat`, `review` (code analysis), `agent` (task completion).
- **Extensible**: Config for models, Tor proxy (like aPEX), Aider-style edits.
- **Windows-Native**: Batch installer, cmd/Warp compatible.

## Quick Setup (Windows)
1. Download/run [Ollama](https://ollama.com/download) installer.
2. In Warp/CMD:
   ```
   install.bat
   ```
3. Test:
   ```
   warpai --help
   warpai chat \"Hello, WarpAI!\"
   ```

## Usage in Warp
Run commands in Warp for interactive features:
```
warpai agent --task \"Write a Python hello world script\"
warpai review myfile.py
warpai chat --model mistral \"Explain Warp Agent Mode\"
```

Paste outputs into Warp's rich editor for #️⃣ blocks, workflows.

## Advanced
- **Tor Proxy**: Set `TOR_PROXY=socks5://127.0.0.1:9050` env, uses in Ollama client.
- **Aider Integration**: `warpai aider --file main.py --message \"fix bug\"` (installs aider).
- **Custom Models**: Edit `config.yaml`.

## No Paid AI Paths
| Method | Cost | UIX |
|--------|------|-----|
| Native Warp Oz | Free 40/mo | Full |
| **ZPI-WARPAI** | $0 | Full (CLI) |
| BYOK | $20/mo | Full |
| Enterprise BYOLLM | $$$ | Full |

## Links
- [Warp Agents](https://docs.warp.dev/agent-platform/warp-agents/warp-agents)
- [Ollama](https://ollama.com/)
- [Aider](https://aider.chat/)

© ZPI-WARPAI | Local WarpAI Unleashed.

