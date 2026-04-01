"""
Runtime executor for ClearCom AST.
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

    if node.type == 'number':
        return node.children[0]

    if node.type == 'id':
        name = node.children[0]
        if name not in values:
            raise NameError(f"Variable '{name}' has no runtime value")
        return values[name]

    if node.type == 'binop':
        op = node.children[0]
        left = _eval_expr(node.children[1], values, symbols)
        right = _eval_expr(node.children[2], values, symbols)
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


def execute_program(ast, symbol_table):
    """Execute AST and return output/value snapshots."""
    result = RuntimeResult()
    values = {}
    symbols = symbol_table.symbols

    if ast is None or ast.type != 'program':
        return result

    for stmt in ast.children:
        try:
            if stmt.type == 'declaration':
                var_type = stmt.children[0]
                var_name = stmt.children[1]
                values[var_name] = 0 if var_type == 'int' else 0.0

            elif stmt.type == 'assignment':
                var_name = stmt.children[0]
                expr = stmt.children[1]
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

            elif stmt.type == 'print':
                arg = stmt.children[0] if stmt.children else None
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
                    val = _eval_expr(arg, values, symbols)
                    result.output_lines.append(str(val))

        except Exception as exc:
            result.runtime_errors.append(str(exc))

    result.values = values
    return result
