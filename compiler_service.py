"""
Shared compile pipeline for ClearCom.
Provides structured results for CLI and web usage.
"""

import re

from lexer import build_lexer
from parser import parse, get_errors, get_symbol_table
from executor import execute_program


def format_source_code(source_code):
    """Lightweight formatter for ClearCom code."""
    text = source_code.replace("\t", "    ")
    # Normalize operator spacing (keeps decimals and strings untouched in most cases).
    text = re.sub(r"\s*([=+\-*/%<>!,])\s*", r" \1 ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" ;", ";").replace(" ,", ",")
    text = text.replace("( ", "(").replace(" )", ")")
    text = text.replace("{ ", "{\n").replace(" }", "\n}")

    tokens = []
    current = []
    for ch in text:
        if ch in "{};\n":
            part = "".join(current).strip()
            if part:
                tokens.append(part)
            tokens.append(ch)
            current = []
        else:
            current.append(ch)
    tail = "".join(current).strip()
    if tail:
        tokens.append(tail)

    lines = []
    indent = 0
    for tok in tokens:
        if tok == "}":
            indent = max(0, indent - 1)
            lines.append("    " * indent + "}")
            continue
        if tok == "{":
            lines.append("    " * indent + "{")
            indent += 1
            continue
        if tok == ";":
            if lines:
                lines[-1] = lines[-1] + ";"
            continue
        if tok == "\n":
            continue
        lines.append("    " * indent + tok)

    return "\n".join(lines).strip()


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


def _safe_label(value):
    text = str(value)
    return text.replace('"', "'")


def _build_ast_mermaid(ast):
    if not ast:
        return "graph TD\n  n0[No AST]"

    lines = ["graph TD"]
    counter = {"id": 0}

    def next_id():
        counter["id"] += 1
        return f"n{counter['id']}"

    def walk(node, parent=None):
        node_id = next_id()

        if isinstance(node, tuple):
            kind = _safe_label(node[0])
            lines.append(f"  {node_id}[\"{kind}\"]")
            if parent:
                lines.append(f"  {parent} --> {node_id}")
            for child in node[1:]:
                walk(child, node_id)
            return

        if isinstance(node, list):
            lines.append(f"  {node_id}[\"list\"]")
            if parent:
                lines.append(f"  {parent} --> {node_id}")
            for child in node:
                walk(child, node_id)
            return

        label = _safe_label(node)
        lines.append(f"  {node_id}[\"{label}\"]")
        if parent:
            lines.append(f"  {parent} --> {node_id}")

    root_id = next_id()
    lines.append(f"  {root_id}[\"program\"]")
    for stmt in ast:
        walk(stmt, root_id)

    return "\n".join(lines)


def _generate_ir(ast):
    instructions = []
    temp_idx = 0
    label_idx = 0

    def next_temp():
        nonlocal temp_idx
        temp_idx += 1
        return f"t{temp_idx}"

    def next_label(prefix="L"):
        nonlocal label_idx
        label_idx += 1
        return f"{prefix}{label_idx}"

    def emit_expr(expr):
        if expr is None:
            return "0"

        kind = expr[0]
        if kind == 'number':
            return str(expr[1])
        if kind == 'id':
            return str(expr[1])
        if kind == 'binop':
            op = expr[1]
            left = emit_expr(expr[2])
            right = emit_expr(expr[3])
            tmp = next_temp()
            instructions.append(f"{tmp} = {left} {op} {right}")
            return tmp

        return f"<{kind}>"

    def emit_stmt(stmt):
        if not stmt:
            return

        kind = stmt[0]

        if kind == 'block':
            for child in stmt[1]:
                emit_stmt(child)
            return

        if kind == 'declaration':
            instructions.append(f"declare {stmt[1]} {stmt[2]}")
            return

        if kind == 'assignment':
            val = emit_expr(stmt[2])
            instructions.append(f"{stmt[1]} = {val}")
            return

        if kind == 'print':
            arg = stmt[1] if len(stmt) > 1 else None
            if isinstance(arg, tuple) and arg[0] == 'string':
                instructions.append(f"print \"{arg[1]}\"")
            elif isinstance(arg, tuple) and arg[0] == 'format_expr':
                val = emit_expr(arg[2])
                instructions.append(f"printf \"{arg[1]}\", {val}")
            elif isinstance(arg, tuple) and arg[0] == 'label_expr':
                val = emit_expr(arg[2])
                instructions.append(f"print \"{arg[1]}\", {val}")
            else:
                expr = arg[1] if isinstance(arg, tuple) and arg[0] == 'expr' else arg
                val = emit_expr(expr)
                instructions.append(f"print {val}")
            return

        if kind == 'if':
            _, cond, then_stmt, else_stmt = stmt
            l_then = next_label("THEN")
            l_else = next_label("ELSE")
            l_end = next_label("ENDIF")
            c = emit_expr(cond)
            instructions.append(f"if {c} goto {l_then}")
            instructions.append(f"goto {l_else}")
            instructions.append(f"label {l_then}")
            emit_stmt(then_stmt)
            instructions.append(f"goto {l_end}")
            instructions.append(f"label {l_else}")
            if else_stmt is not None:
                emit_stmt(else_stmt)
            instructions.append(f"label {l_end}")
            return

        if kind == 'while':
            _, cond, body = stmt
            l_start = next_label("WHILE_START")
            l_body = next_label("WHILE_BODY")
            l_end = next_label("WHILE_END")
            instructions.append(f"label {l_start}")
            c = emit_expr(cond)
            instructions.append(f"if {c} goto {l_body}")
            instructions.append(f"goto {l_end}")
            instructions.append(f"label {l_body}")
            emit_stmt(body)
            instructions.append(f"goto {l_start}")
            instructions.append(f"label {l_end}")
            return

        if kind == 'for':
            _, init, cond, update, body = stmt
            l_start = next_label("FOR_START")
            l_body = next_label("FOR_BODY")
            l_end = next_label("FOR_END")
            if init is not None:
                emit_stmt(init)
            instructions.append(f"label {l_start}")
            if cond is not None:
                c = emit_expr(cond)
                instructions.append(f"if {c} goto {l_body}")
                instructions.append(f"goto {l_end}")
            else:
                instructions.append(f"goto {l_body}")
            instructions.append(f"label {l_body}")
            emit_stmt(body)
            if update is not None:
                emit_stmt(update)
            instructions.append(f"goto {l_start}")
            instructions.append(f"label {l_end}")
            return

        instructions.append(f"; unknown statement {kind}")

    for statement in ast or []:
        emit_stmt(statement)

    return instructions


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
    elif "never used" in lower or "possible keyword typo" in lower:
        category = "Warning"
        hint = "Review this warning and update code if needed."
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


def compile_source(source_code, trace=False):
    """Compile source text and return a structured result."""
    unsupported_errors = _find_unsupported_construct_errors(source_code)
    if unsupported_errors:
        diagnostics = [_error_to_diagnostic(err) for err in unsupported_errors]
        return {
            "success": False,
            "errors": unsupported_errors,
            "warnings": [],
            "diagnostics": diagnostics,
            "tokens": [],
            "symbols": {},
            "ast": [],
            "astMermaid": "graph TD\n  n0[No AST]",
            "ir": [],
            "trace": [],
            "stages": [
                {"name": "Lexical Analysis", "status": "skipped", "detail": "Stopped before lexing due to unsupported construct."},
                {"name": "Syntax Parsing", "status": "skipped", "detail": "Stopped before parsing."},
                {"name": "Semantic Analysis", "status": "skipped", "detail": "Stopped before semantic checks."},
                {"name": "IR Generation", "status": "skipped", "detail": "No AST available for IR."},
                {"name": "Execution", "status": "failed", "detail": "Compilation stopped due to unsupported construct."},
            ],
            "output": [],
        }

    tokens = _tokenize(source_code)

    lexer = build_lexer()
    parsed_program = parse(source_code, lexer)

    lexer_errors = lexer.errors
    lexer_warnings = lexer.warnings
    semantic_and_parser_errors = get_errors()
    semantic_warnings = get_symbol_table().get_unused_warnings()
    symbol_table = get_symbol_table()
    symbols = dict(symbol_table.symbols)

    runtime_output = []
    runtime_errors = []
    runtime_values = {}
    runtime_trace = []

    if parsed_program:
        runtime = execute_program(parsed_program, symbol_table, trace=trace)
        runtime_output = runtime.output_lines
        runtime_errors = runtime.runtime_errors
        runtime_values = runtime.values
        runtime_trace = runtime.trace_lines

    ir_instructions = _generate_ir(parsed_program if parsed_program else [])
    ast_mermaid = _build_ast_mermaid(parsed_program if parsed_program else [])

    errors = lexer_errors + semantic_and_parser_errors + runtime_errors
    warnings = lexer_warnings + semantic_warnings
    diagnostics = [_error_to_diagnostic(err) for err in errors]
    diagnostics.extend(_error_to_diagnostic(warn) for warn in warnings)

    stages = [
        {
            "name": "Lexical Analysis",
            "status": "ok" if not lexer_errors else "failed",
            "detail": f"Generated {len(tokens)} tokens.",
        },
        {
            "name": "Syntax Parsing",
            "status": "ok" if parsed_program is not None else "failed",
            "detail": "AST built." if parsed_program is not None else "AST generation failed.",
        },
        {
            "name": "Semantic Analysis",
            "status": "ok" if not semantic_and_parser_errors else "failed",
            "detail": f"Tracked {len(symbols)} symbols.",
        },
        {
            "name": "IR Generation",
            "status": "ok" if parsed_program is not None else "skipped",
            "detail": f"Generated {len(ir_instructions)} IR instructions." if parsed_program is not None else "No AST to convert.",
        },
        {
            "name": "Execution",
            "status": "ok" if not runtime_errors else "failed",
            "detail": f"Produced {len(runtime_output)} output line(s)." if not runtime_errors else f"Runtime issues: {len(runtime_errors)}",
        },
    ]

    return {
        "success": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "diagnostics": diagnostics,
        "tokens": tokens,
        "symbols": symbols,
        "ast": parsed_program if parsed_program else [],
        "astMermaid": ast_mermaid,
        "ir": ir_instructions,
        "trace": runtime_trace,
        "stages": stages,
        "output": runtime_output,
        "runtimeValues": runtime_values,
    }
