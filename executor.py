"""
Runtime executor for parsed ClearCom statements.
Evaluates statements and collects program output.
"""


class RuntimeResult:
    def __init__(self):
        self.output_lines = []
        self.runtime_errors = []
        self.values = {}


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
            return left / right
        if op == '%':
            return left % right
        raise ValueError(f"Unsupported operator '{op}'")

    raise ValueError("Unknown expression node")


def execute_program(parsed_program, symbol_table):
    """Execute parsed statements and return output/value snapshots."""
    result = RuntimeResult()
    values = {}
    symbols = symbol_table.symbols

    if not parsed_program:
        return result

    for stmt in parsed_program:
        try:
            if stmt[0] == 'declaration':
                var_type = stmt[1]
                var_name = stmt[2]
                values[var_name] = 0 if var_type == 'int' else 0.0

            elif stmt[0] == 'assignment':
                var_name = stmt[1]
                expr = stmt[2]
                value = _eval_expr(expr, values, symbols)

                var_type = symbols.get(var_name)
                if var_type == 'int':
                    if isinstance(value, float) and not value.is_integer():
                        result.runtime_errors.append(
                            f"Type mismatch at runtime: cannot assign float {value} to int '{var_name}'"
                        )
                        continue
                    values[var_name] = int(value)
                else:
                    values[var_name] = float(value)

            elif stmt[0] == 'print':
                arg = stmt[1] if len(stmt) > 1 else None
                if isinstance(arg, tuple) and arg[0] == 'string':
                    result.output_lines.append(arg[1])
                elif isinstance(arg, tuple) and arg[0] == 'format_expr':
                    fmt = arg[1]
                    val = _eval_expr(arg[2], values, symbols)
                    if '%d' in fmt:
                        result.output_lines.append(fmt.replace('%d', str(int(val))))
                    elif '%f' in fmt:
                        result.output_lines.append(fmt.replace('%f', str(float(val))))
                    else:
                        result.output_lines.append(f"{fmt} {val}")
                else:
                    expr = arg[1] if isinstance(arg, tuple) and arg[0] == 'expr' else arg
                    val = _eval_expr(expr, values, symbols)
                    result.output_lines.append(str(val))

        except Exception as exc:
            result.runtime_errors.append(str(exc))

    result.values = values
    return result
