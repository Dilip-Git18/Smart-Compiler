"""
Shared compile pipeline for ClearCom.
Provides structured results for CLI and web usage.
"""

import re

from lexer import build_lexer
from parser import parse, get_errors, get_symbol_table
from executor import execute_program


def _tokenize(source_code):
    lexer = build_lexer()
    lexer.input(source_code)
    tokens = []
    for token in lexer:
        tokens.append(
            {
                "type": token.type,
                "value": token.value,
                "line": token.lineno,
            }
        )
    return tokens


def _error_to_diagnostic(error_msg):
    lower = error_msg.lower()
    line_match = re.search(r"Line\s+(\d+):", error_msg)
    line = int(line_match.group(1)) if line_match else None

    if "unsupported character" in lower:
        category = "Lexical"
        hint = "Use only supported ClearCom syntax and remove unsupported symbols."
    elif "unsupported construct" in lower:
        category = "Language Limit"
        hint = "Use declarations, assignments, arithmetic expressions, print, printf, and optional int main(){...}."
    elif "undeclared variable" in lower:
        category = "Semantic"
        hint = "Declare the variable first, e.g., int x; before using x."
    elif "duplicate variable" in lower:
        category = "Semantic"
        hint = "Variable already exists. Rename it or remove the duplicate declaration."
    elif "unknown function" in lower:
        category = "Semantic"
        hint = "Use supported calls: print(expr); or printf(\"text\");"
    elif "missing ';' after" in lower:
        category = "Syntax"
        hint = "Add a semicolon ';' at the end of the statement."
    elif "syntax error" in lower or "invalid statement" in lower:
        category = "Syntax"
        hint = "Check token spelling and statement format. Use declarations, assignments, print/printf, if/else, while, and for."
    elif "type mismatch" in lower or "runtime" in lower:
        category = "Runtime"
        hint = "Match variable types in assignments and expressions."
    else:
        category = "General"
        hint = "Review the statement and fix the reported issue."

    return {
        "line": line,
        "category": category,
        "message": error_msg,
        "hint": hint,
    }


def _find_unsupported_construct_errors(source_code):
    errors = []
    lines = source_code.splitlines()
    checks = [
        ("scanf", "scanf is not supported; use fixed assignments and print/printf"),
    ]

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        for keyword, note in checks:
            if line.startswith(f"{keyword}(") or line.startswith(f"{keyword} "):
                errors.append(f"Line {idx}: Unsupported construct '{keyword}' ({note})")

    return errors


def compile_source(source_code):
    """Compile source text and return a structured result."""
    unsupported_errors = _find_unsupported_construct_errors(source_code)
    if unsupported_errors:
        diagnostics = [_error_to_diagnostic(err) for err in unsupported_errors]
        return {
            "success": False,
            "errors": unsupported_errors,
            "diagnostics": diagnostics,
            "tokens": [],
            "symbols": {},
            "ast": [],
            "output": [],
        }

    lexer = build_lexer()
    parsed_program = parse(source_code, lexer)

    lexer_errors = lexer.errors
    semantic_and_parser_errors = get_errors()
    symbol_table = get_symbol_table()
    symbols = dict(symbol_table.symbols)

    runtime_output = []
    runtime_errors = []

    if parsed_program:
        runtime = execute_program(parsed_program, symbol_table)
        runtime_output = runtime.output_lines
        runtime_errors = runtime.runtime_errors

    errors = lexer_errors + semantic_and_parser_errors + runtime_errors
    diagnostics = [_error_to_diagnostic(err) for err in errors]

    return {
        "success": len(errors) == 0,
        "errors": errors,
        "diagnostics": diagnostics,
        "tokens": _tokenize(source_code),
        "symbols": symbols,
        "ast": parsed_program if parsed_program else [],
        "output": runtime_output,
    }
