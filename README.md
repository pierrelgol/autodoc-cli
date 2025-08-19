# autodoc-cli

A command-line tool that automatically generates and updates documentation for your code using AI.

## Features

- 🤖 **AI-Powered**: Uses Ollama to generate intelligent documentation
- 🔄 **Smart Updates**: Only updates documentation when code changes
- 📝 **Multi-Language**: Currently supports C (more languages coming soon)
- 💾 **Persistent Storage**: Tracks changes using SQLite database
- 🎯 **Precise**: Uses Tree-sitter for accurate code parsing

## Binary Installation (Recommended)

Download the latest binary for your platform from [GitHub Releases](https://github.com/pierrelgol/autodoc-cli/releases):

### Linux
```bash
# Download and make executable
wget https://github.com/pierrelgol/autodoc-cli/releases/latest/download/autodoc-linux-x86_64
chmod +x autodoc-linux-x86_64
./autodoc-linux-x86_64 --help
```

### macOS
```bash
# Download and make executable
wget https://github.com/pierrelgol/autodoc-cli/releases/latest/download/autodoc-macos-x86_64
chmod +x autodoc-macos-x86_64
./autodoc-macos-x86_64 --help
```

### Windows
```bash
# Download and run
curl -L -o autodoc-windows-x86_64.exe https://github.com/pierrelgol/autodoc-cli/releases/latest/download/autodoc-windows-x86_64.exe
./autodoc-windows-x86_64.exe --help
```

**Note**: The binary includes a fallback mechanism that can build tree-sitter grammars from source if the bundled ones fail to load. This requires the `tree-sitter` CLI tool to be installed:

```bash
# Install tree-sitter CLI (required for fallback)
npm install -g tree-sitter-cli
```

## Python Package Installation

```bash
pip install autodoc-cli
```

## Development Installation

```bash
# Clone the repository
git clone https://github.com/pierrelgol/autodoc-cli.git
cd autodoc-cli

# Create virtual environment and install in development mode
uv venv --python 3.12
uv pip install -e .[dev]
```

## Usage

### Basic Usage

```bash
# Generate documentation for a directory
autodoc /path/to/your/code

# Use a specific Ollama model
autodoc /path/to/your/code --model llama3.2:3b

# Preview changes without modifying files
autodoc /path/to/your/code --dry-run
```

### Options

- `--model`: Ollama model name/tag (default: `qwen2.5-coder:7b`)
- `--db`: Path to SQLite database (defaults to `.autodoc.sqlite` in project root)
- `--dry-run`: Do not modify files; print planned changes

## Requirements

- **Ollama**: Must be running locally with the specified model
- **Tree-sitter CLI**: Required for fallback grammar building (install via `npm install -g tree-sitter-cli`)

## How It Works

1. **Scans** your code directory recursively
2. **Parses** code using Tree-sitter for accurate AST analysis
3. **Tracks** changes using a SQLite database
4. **Generates** documentation using Ollama AI
5. **Updates** only when code has actually changed

## Fallback Mechanism

If the bundled tree-sitter grammars fail to load (common in PyInstaller binaries), the tool will automatically:

1. Detect the failure
2. Clone the grammar repository from GitHub
3. Build the grammar from source using `tree-sitter generate`
4. Load the freshly built grammar

This ensures the tool works reliably across different platforms and environments.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.


