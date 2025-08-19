from __future__ import annotations

import os
import subprocess
from typing import Iterable, Optional

from tree_sitter import Language, Parser
from tree_sitter_languages import get_language

from .base import ByteRange, FunctionInfo, LanguageAdapter


def _build_language_grammar(language_name: str) -> Language:
    """Build a tree-sitter language grammar from source when bundled version fails."""
    # Check if tree-sitter CLI is available
    try:
        subprocess.run(["tree-sitter", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  tree-sitter CLI not found. Please install it first:")
        print("   npm install -g tree-sitter-cli")
        print("   or visit: https://tree-sitter.github.io/tree-sitter/creating-parsers#installation")
        raise RuntimeError("tree-sitter CLI is required for building grammars from source")
    
    # Create a temporary directory for building
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the grammar repository
        grammar_repo = f"https://github.com/tree-sitter/tree-sitter-{language_name}"
        print(f"🔨 Building {language_name} grammar from source...")
        print(f"📥 Cloning {grammar_repo}")
        
        subprocess.check_call(["git", "clone", "--depth", "1", grammar_repo, temp_dir])
        
        # Build the grammar
        print("🔨 Building grammar...")
        subprocess.check_call(["tree-sitter", "generate"], cwd=temp_dir)
        
        # Load the built language
        language_path = os.path.join(temp_dir, "src", "tree_sitter_parser")
        return Language(language_path, language_name)


class CAdapter(LanguageAdapter):
    language_name = "c"

    def __init__(self) -> None:
        # Initialize parser for C with fallback to building from source
        try:
            self.language: Language = get_language("c")
        except (OSError, ImportError) as e:
            print(f"⚠️  Failed to load bundled C grammar: {e}")
            print("🔄 Attempting to build from source...")
            self.language = _build_language_grammar("c")
        
        self.parser: Parser = Parser()
        self.parser.set_language(self.language)

    def iter_functions(self, source_code: bytes) -> Iterable[FunctionInfo]:
        tree = self.parser.parse(bytes(source_code))
        root = tree.root_node

        # We consider function_definition nodes. We avoid regex; we rely on the grammar.
        for current in self._walk(root):
            if current.type == "function_definition":
                yield self._extract_function_info(source_code, current)

    # Helper traversal to iterate all nodes
    def _walk(self, node) -> Iterable:
        stack = [node]
        while stack:
            n = stack.pop()
            yield n
            for child in reversed(n.children):
                stack.append(child)

    def _extract_function_info(self, source_code: bytes, node) -> FunctionInfo:
        # Extract function information from tree-sitter AST node.
        # Optional preceeding comment nodes will be identified by scanning preceding siblings that are comments.

        # Find name
        name = ""
        body_node = None
        declarator = None
        for child in node.children:
            if child.type == "compound_statement":
                body_node = child
            if "declarator" in child.type:
                declarator = child
        if declarator is not None:
            # search for identifier under declarator
            for d_child in self._walk(declarator):
                if d_child.type == "identifier":
                    name = source_code[d_child.start_byte : d_child.end_byte].decode("utf-8", errors="replace")
                    break

        # Determine ranges
        full_range = ByteRange(start=node.start_byte, end=node.end_byte)
        body_range = ByteRange(start=body_node.start_byte if body_node else node.start_byte, end=body_node.end_byte if body_node else node.end_byte)
        signature_end = declarator.end_byte if declarator else node.start_byte
        signature_range = ByteRange(start=node.start_byte, end=signature_end)

        # Detect leading doc comment range by scanning immediate preceding comments.
        doc_range: Optional[ByteRange] = None
        prev = node.prev_sibling
        if prev is not None and prev.type == "comment":
            # Accumulate contiguous leading comments immediately above, stopping when encountering blank or non-comment
            start = prev.start_byte
            end = prev.end_byte
            cursor = prev.prev_sibling
            contiguous = True
            while cursor is not None and contiguous:
                if cursor.type == "comment":
                    # ensure there is only whitespace/newlines between comments
                    between = source_code[cursor.end_byte : start]
                    if between.strip():
                        break
                    start = cursor.start_byte
                    cursor = cursor.prev_sibling
                else:
                    break
            doc_range = ByteRange(start=start, end=end)

        return FunctionInfo(
            name=name or "",
            signature_range=signature_range,
            body_range=body_range,
            full_range=full_range,
            doc_range=doc_range,
        )


