AutoDoc
=======

CLI tool that generates documentation comments for source code using Tree-sitter parsing and a local Ollama model. Initially supports C (`.c`, `.h`).

Requirements
------------
- Python 3.13+
- `uv` for environment management
- Ollama running locally with a compatible code model (e.g., `qwen2.5-coder:7b`)

Install
-------

```bash
uv venv && source .venv/bin/activate
uv pip install -e .[dev]
```

Usage
-----

```bash
source .venv/bin/activate
autodoc /path/to/target --model qwen2.5-coder:7b
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

Notes
-----
- Only C is supported currently. Additional languages can be added by implementing the `LanguageAdapter` interface in `autodoc/adapters`.
- Ensure Ollama is running locally: `ollama serve` and that the model is available: `ollama pull qwen2.5-coder:7b`.
- If you prefer uvx, be aware that `uvx autodoc` may resolve to the PyPI package named `autodoc`. Use the local script instead: `.venv/bin/autodoc`.


