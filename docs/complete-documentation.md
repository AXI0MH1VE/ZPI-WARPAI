# ZPI-WARPAI - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Usage Examples](#usage-examples)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Project Overview

ZPI-WARPAI is a local-only AI coding agent designed to run inside the Warp terminal. It provides a complete alternative to cloud-based AI coding assistants by using local language models via Ollama, eliminating subscription costs and privacy concerns.

### Key Features
- **Local-Only Operation**: All AI processing happens on your machine
- **Warp Integration**: Full UIX features including rich output and syntax highlighting
- **Multiple Modes**: Chat, review, and agent modes for different workflows
- **Aider Integration**: Git-native code editing capabilities
- **Windows Native**: Designed specifically for Windows environments

## System Requirements

### Hardware Requirements
- **RAM**: Minimum 8GB (16GB+ recommended for larger models)
- **Storage**: 10GB+ free space for models and dependencies
- **CPU**: Modern multi-core processor
- **GPU**: Optional but recommended for faster inference

### Software Requirements
- **Windows 10 or 11**
- **Python 3.8+**
- **Ollama** (download from https://ollama.com/download)
- **Warp Terminal** (download from https://warp.dev)

## Installation Guide

### Step 1: Install Ollama
1. Download Ollama from https://ollama.com/download
2. Run the installer and follow the setup wizard
3. Start the Ollama service (it runs automatically on Windows)

### Step 2: Install ZPI-WARPAI
1. Clone or download the ZPI-WARPAI project
2. Navigate to the project directory in your terminal
3. Run the installation script:

```bash
# For Windows users
.\install.bat

# For manual installation
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2:3b
```

### Step 3: Verify Installation
1. Activate the virtual environment:
```bash
.\.venv\Scripts\activate
```

2. Test the installation:
```bash
warpai --help
```

3. Test with a simple command:
```bash
warpai chat "Hello, WarpAI!"
```

## Configuration

### Configuration File
The main configuration is stored in `config.yaml`:

```yaml
default_model: llama3.2:3b
ollama_host: http://localhost:11434
tor_proxy: null  # socks5://127.0.0.1:9050 for Tor
aider_enabled: true
```

### Available Configuration Options
- `default_model`: The Ollama model to use (default: llama3.2:3b)
- `ollama_host`: URL of the Ollama server
- `tor_proxy`: Optional Tor proxy configuration
- `aider_enabled`: Enable/disable Aider integration

### Environment Variables
- `TOR_PROXY`: Set Tor proxy URL (overrides config.yaml)
- `OLLAMA_HOST`: Set custom Ollama server URL

## Usage Examples

### Basic Chat Mode
```bash
# Start chat with default model
warpai chat

# Start chat with specific model
warpai chat --model mistral

# Chat with initial message
warpai chat "Explain Python decorators"
```

### Review Mode
```bash
# Analyze a Python file
warpai review my_script.py

# Analyze multiple files
warpai review file1.py file2.py
```

### Agent Mode
```bash
# Complete a specific task
warpai agent --task "Write a Python hello world script"

# Work on specific files
warpai agent --task "Refactor the main function" --files main.py utils.py
```

### Aider Integration
```bash
# Use Aider commands through warpai
warpai aider --file main.py --message "fix the bug in line 42"
```

## Advanced Features

### Custom Models
You can use any Ollama-compatible model:

```bash
# Pull a different model
ollama pull codellama:7b

# Update config.yaml
default_model: codellama:7b
```

### Tor Proxy Support
For enhanced privacy, configure Tor proxy:

```yaml
tor_proxy: socks5://127.0.0.1:9050
```

### Multiple Model Support
Switch between models for different tasks:

```bash
# Use different models for different tasks
warpai chat --model llama3.2:3b "Write documentation"
warpai agent --model codellama:7b --task "Refactor code"
```

## Troubleshooting

### Common Issues and Solutions

#### Ollama Not Found
```
Error: Ollama not found. Download from https://ollama.com/download
```
**Solution**: Install Ollama from the official website and ensure it's running.

#### Python Environment Issues
```
Error: Python not found. Install from python.org
```
**Solution**: Install Python 3.8+ from https://python.org and ensure it's in your PATH.

#### Model Download Failures
```
Error: Failed to pull model
```
**Solution**: Check your internet connection and disk space. Try again or use a smaller model.

#### Warp Integration Issues
```
Error: Cannot connect to Warp terminal
```
**Solution**: Ensure Warp is installed and running. Check that warpai is executed within a Warp terminal session.

### Debug Mode
Enable debug logging for detailed error information:

```bash
warpai --debug
```

### Log Files
Log files are stored in:
- Windows: `%APPDATA%\warpai\logs\`
- Linux/Mac: `~/.local/share/warpai/logs/`

## FAQ

### Q: Can I use this on macOS or Linux?
A: Yes, but the install.bat script is Windows-specific. Use the manual installation instructions instead.

### Q: What models work best for coding?
A: Code-specific models like CodeLlama, DeepSeek-Coder, or general models like Llama 3 work well. Experiment to find what suits your needs.

### Q: How much RAM do I need?
A: Minimum 8GB for smaller models (3B parameters). 16GB+ recommended for larger models (7B+ parameters).

### Q: Can I use this without Warp?
A: Yes, but you'll lose the rich UIX features. It will work in any terminal that supports basic ANSI escape codes.

### Q: How do I update the models?
A: Use Ollama commands:
```bash
# Update a model
ollama pull llama3.2:3b

# List available models
ollama list
```

### Q: Is my data private?
A: Yes! All processing happens locally on your machine. No data is sent to external servers.

## Performance Tips

1. **Use appropriate model size**: Smaller models are faster but less capable
2. **Close unnecessary applications**: Free up RAM for better performance
3. **Use GPU acceleration**: If available, configure Ollama to use your GPU
4. **Cache models**: Once downloaded, models are cached locally

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the log files
- Create an issue on the GitHub repository
- Join the community Discord (link in README)

---

**Last Updated**: 2026-04-20
**Version**: 1.0.0