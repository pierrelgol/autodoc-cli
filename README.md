AutoDoc
=======

CLI tool that generates documentation comments for source code using Tree-sitter parsing and a local Ollama model. Initially supports C (`.c`, `.h`).

Requirements
------------
- Python 3.12+
- `uv` for environment management
- Ollama running locally with a compatible code model (e.g., `qwen2.5-coder:7b`)

Install
-------

### Binary Installation (Recommended)

Download the latest binary for your platform from the [GitHub releases](https://github.com/pierrelgol/autodoc-cli/releases):

```bash
# Linux
wget https://github.com/pierrelgol/autodoc-cli/releases/latest/download/autodoc-linux-x86_64
chmod +x autodoc-linux-x86_64
./autodoc-linux-x86_64 --help

# macOS
wget https://github.com/pierrelgol/autodoc-cli/releases/latest/download/autodoc-macos-x86_64
chmod +x autodoc-macos-x86_64
./autodoc-macos-x86_64 --help

# Windows
# Download autodoc-windows-x86_64.exe from the releases page
```

### Python Package Installation

```bash
# Install from PyPI
pip install autodoc-cli

# Or using uv
uv pip install autodoc-cli
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/pierrelgol/autodoc-cli.git
cd autodoc-cli

# Create virtual environment and install in development mode
uv venv --python 3.12
uv pip install -e .[dev]

# Build binary locally
./build_binary.sh
```

Usage
-----

```bash
# Basic usage
autodoc /path/to/target --model qwen2.5-coder:7b

# Dry run to see what would be changed
autodoc /path/to/target --dry-run

# Use a different model
autodoc /path/to/target --model llama3.1:8b

# Specify a custom database location
autodoc /path/to/target --db /path/to/custom.db

# Example: Generate documentation for a C project
autodoc /path/to/c-project --model qwen2.5-coder:7b
```

By default, a SQLite DB `.autodoc.sqlite` will be created in the target directory to track function body hashes for change detection.

How it works
------------
- Tree-sitter is used to parse C files into ASTs. No regex is used for detection.
- For each function:
  - If a doc comment exists and the function hash matches the DB, the function is skipped.
  - If a doc exists but the hash changed, the doc is regenerated and replaced.
  - If no doc exists, a new doc comment is generated and inserted above the function.
- Edits are applied directly to the source files and are idempotent.

Example
-------

Before running autodoc:
```c
int calculate_fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2);
}
```

After running `autodoc . --model qwen2.5-coder:7b`:
```c
/**
 * Calculates the nth Fibonacci number using recursion.
 *
 * @param n The position in the Fibonacci sequence (0-based).
 * @return The Fibonacci number at position n.
 */
int calculate_fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2);
}
```

Notes
-----
- Only C is supported currently. Additional languages can be added by implementing the `LanguageAdapter` interface in `autodoc/adapters`.
- Ensure Ollama is running locally: `ollama serve` and that the model is available: `ollama pull qwen2.5-coder:7b`.
- If you prefer uvx, be aware that `uvx autodoc` may resolve to the PyPI package named `autodoc`. Use the local script instead: `.venv/bin/autodoc`.


