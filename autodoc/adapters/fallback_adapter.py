from __future__ import annotations

import re
from typing import Iterable

from .base import ByteRange, FunctionInfo, LanguageAdapter


class FallbackCAdapter(LanguageAdapter):
    """Fallback C adapter that uses regex-based parsing when tree-sitter is not available."""
    language_name = "c"

    def __init__(self) -> None:
        # Simple regex patterns for C function detection
        self.function_pattern = re.compile(
            r'(\w+(?:\s+\w+)*)\s+(\w+)\s*\([^)]*\)\s*\{',  # Basic function pattern
            re.MULTILINE | re.DOTALL
        )
        self.comment_pattern = re.compile(
            r'/\*\*.*?\*/',  # Doc comment pattern
            re.MULTILINE | re.DOTALL
        )

    def iter_functions(self, source_code: bytes) -> Iterable[FunctionInfo]:
        """Extract function information using regex patterns."""
        source_str = source_code.decode('utf-8', errors='replace')
        
        # Find all potential function matches
        for match in self.function_pattern.finditer(source_str):
            start_pos = match.start()
            end_pos = match.end()
            
            # Find the function body end (matching brace)
            brace_count = 0
            body_start = source_str.find('{', start_pos)
            if body_start == -1:
                continue
                
            body_start += 1  # Skip the opening brace
            body_end = body_start
            
            for i, char in enumerate(source_str[body_start:], body_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    if brace_count == 0:
                        body_end = i
                        break
                    brace_count -= 1
            
            if body_end <= body_start:
                continue
            
            # Extract function name and return type
            full_match = match.group(0)
            return_type = match.group(1).strip()
            func_name = match.group(2).strip()
            
            # Find signature end (before the opening brace)
            signature_end = source_str.find('{', start_pos)
            if signature_end == -1:
                continue
            
            # Look for preceding doc comment
            doc_range = None
            comment_start = source_str.rfind('/**', 0, start_pos)
            if comment_start != -1:
                comment_end = source_str.find('*/', comment_start)
                if comment_end != -1:
                    comment_end += 2  # Include the closing */
                    # Check if there's only whitespace between comment and function
                    between = source_str[comment_end:start_pos].strip()
                    if not between or between.startswith('\n'):
                        doc_range = ByteRange(
                            start=comment_start,
                            end=comment_end
                        )
            
            yield FunctionInfo(
                name=func_name,
                signature_range=ByteRange(start=start_pos, end=signature_end),
                body_range=ByteRange(start=body_start, end=body_end),
                full_range=ByteRange(start=start_pos, end=body_end + 1),  # Include closing brace
                doc_range=doc_range
            )
