"""
Runtime executor for parsed ClearCom statements.
Evaluates statements and collects program output.
"""


class RuntimeResult:
    def __init__(self):
        self.output_lines = []
        self.runtime_errors = []
        self.values = {}
        self.trace_lines = []


def _eval_expr(node, values, symbols):
    if node is None:
        raise ValueError("Invalid expression")

    kind = node[0]

    if kind == 'number':
        return node[1]

    if kind == 'id':
        name = node[1]
        if name not in values:
            raise NameError(f"Variable '{name}' has no runtime value")
        return values[name]

    if kind == 'binop':
        op = node[1]
        left = _eval_expr(node[2], values, symbols)
        right = _eval_expr(node[3], values, symbols)
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right
        if op == '%':
            if right == 0:
                raise ZeroDivisionError("Modulo by zero")
            return left % right
        if op == '<':
            return 1 if left < right else 0
        if op == '<=':
            return 1 if left <= right else 0
        if op == '>':
            return 1 if left > right else 0
        if op == '>=':
            return 1 if left >= right else 0
        if op == '==':
            return 1 if left == right else 0
        if op == '!=':
            return 1 if left != right else 0
        raise ValueError(f"Unsupported operator '{op}'")

    raise ValueError("Unknown expression node")


def execute_program(parsed_program, symbol_table, trace=False):
    """Execute parsed statements and return output/value snapshots."""
    result = RuntimeResult()
    values = {}
    symbols = symbol_table.symbols

    if not parsed_program:
        return result

    def _assign(var_name, expr):
        value = _eval_expr(expr, values, symbols)
        var_type = symbols.get(var_name)
        if var_type == 'int':
            if isinstance(value, float) and not value.is_integer():
                raise TypeError(
                    f"Type mismatch at runtime: cannot assign float {value} to int '{var_name}'"
                )
            values[var_name] = int(value)
        else:
            values[var_name] = float(value)

        if trace:
            result.trace_lines.append(f"assign {var_name} = {values[var_name]}")

    def _truthy(expr):
        return _eval_expr(expr, values, symbols) != 0

    def _exec_statement(stmt):
        if not stmt:
            return

        kind = stmt[0]

        if kind == 'block':
            _exec_block(stmt[1])
            return

        if kind == 'declaration':
            var_type = stmt[1]
            var_name = stmt[2]
            values[var_name] = 0 if var_type == 'int' else 0.0
            if trace:
                result.trace_lines.append(f"declare {var_type} {var_name} = {values[var_name]}")
            return

        if kind == 'assignment':
            _assign(stmt[1], stmt[2])
            return

        if kind == 'if':
            _, cond, then_stmt, else_stmt = stmt
            cond_val = _eval_expr(cond, values, symbols)
            if trace:
                result.trace_lines.append(f"if cond={cond_val}")
            if cond_val != 0:
                _exec_statement(then_stmt)
            elif else_stmt is not None:
                _exec_statement(else_stmt)
            return

        if kind == 'while':
            _, cond, body = stmt
            loop_guard = 0
            while _eval_expr(cond, values, symbols) != 0:
                if trace:
                    result.trace_lines.append(f"while iter={loop_guard + 1}")
                _exec_statement(body)
                loop_guard += 1
                if loop_guard > 100000:
                    raise RuntimeError("Loop limit exceeded (possible infinite loop)")
            return

        if kind == 'for':
            _, init, cond, update, body = stmt
            if init is not None:
                _exec_statement(init)

            loop_guard = 0
            while True:
                if cond is not None and not _truthy(cond):
                    break
                if trace:
                    result.trace_lines.append(f"for iter={loop_guard + 1}")
                _exec_statement(body)
                if update is not None:
                    _exec_statement(update)
                loop_guard += 1
                if loop_guard > 100000:
                    raise RuntimeError("Loop limit exceeded (possible infinite loop)")
            return

        if kind == 'print':
            arg = stmt[1] if len(stmt) > 1 else None
            if isinstance(arg, tuple) and arg[0] == 'string':
                line = arg[1]
                result.output_lines.append(line)
                if trace:
                    result.trace_lines.append(f"print {line}")
            elif isinstance(arg, tuple) and arg[0] == 'format_expr':
                fmt = arg[1]
                val = _eval_expr(arg[2], values, symbols)
                if '%d' in fmt:
                    line = fmt.replace('%d', str(int(val)))
                    result.output_lines.append(line)
                elif '%f' in fmt:
                    line = fmt.replace('%f', str(float(val)))
                    result.output_lines.append(line)
                else:
                    line = f"{fmt} {val}"
                    result.output_lines.append(line)
                if trace:
                    result.trace_lines.append(f"print {line}")
            elif isinstance(arg, tuple) and arg[0] == 'label_expr':
                label = arg[1]
                val = _eval_expr(arg[2], values, symbols)
                line = f"{label}{val}"
                result.output_lines.append(line)
                if trace:
                    result.trace_lines.append(f"print {line}")
            else:
                expr = arg[1] if isinstance(arg, tuple) and arg[0] == 'expr' else arg
                val = _eval_expr(expr, values, symbols)
                line = str(val)
                result.output_lines.append(line)
                if trace:
                    result.trace_lines.append(f"print {line}")
            return

        raise ValueError(f"Unknown statement kind '{kind}'")

    def _exec_block(statements):
        for stmt in statements:
            _exec_statement(stmt)

    for stmt in parsed_program:
        try:
            _exec_statement(stmt)

        except Exception as exc:
            result.runtime_errors.append(str(exc))

    result.values = values
    return result
