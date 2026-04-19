"""
Parser for ClearCom - Mini C-like Smart Error Detecting Compiler
Performs syntax analysis and semantic checking using PLY
"""

import difflib

try:
    import ply.yacc as yacc
except ImportError as exc:
    raise ImportError(
        "PLY is not installed in the selected Python environment. "
        "Install it with: python3 -m pip install ply"
    ) from exc
from lexer import tokens  # Import tokens from lexer
from symbol_table import SymbolTable    

# Symbol table for semantic analysis
symbol_table = SymbolTable()

# Parser error tracking
parser_errors = []
syntax_error_lines = set()
active_parser = None

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)


def _add_error_once(line, message):
    if line is None:
        if message not in parser_errors:
            parser_errors.append(message)
        return
    if line not in syntax_error_lines:
        parser_errors.append(message)
        syntax_error_lines.add(line)

# ============================================
# Grammar Rules
# ============================================

def p_program(p):
    """program : statement_list
               | INT MAIN LPAREN RPAREN LBRACE statement_list RBRACE"""
    statements = p[1] if len(p) == 2 else p[6]
    p[0] = [stmt for stmt in statements if stmt is not None]

def p_statement_list(p):
    """statement_list : statement
                      | statement_list statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[2]:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = p[1]

def p_statement(p):
    """statement : declaration
                 | assignment
                 | print_stmt
                 | unknown_call_stmt
                 | block_stmt
                 | if_stmt
                 | while_stmt
                 | for_stmt"""
    p[0] = p[1]


def p_block_stmt(p):
    """block_stmt : LBRACE statement_list RBRACE
                  | LBRACE RBRACE"""
    if len(p) == 4:
        p[0] = ('block', p[2])
    else:
        p[0] = ('block', [])


def p_scoped_statement(p):
    """scoped_statement : statement"""
    p[0] = p[1]


def p_if_stmt(p):
    """if_stmt : IF LPAREN expression RPAREN scoped_statement %prec IFX
               | IF LPAREN expression RPAREN scoped_statement ELSE scoped_statement"""
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])


def p_while_stmt(p):
    """while_stmt : WHILE LPAREN expression RPAREN scoped_statement"""
    p[0] = ('while', p[3], p[5])


def p_for_stmt(p):
    """for_stmt : FOR LPAREN for_init_opt SEMICOLON for_cond_opt SEMICOLON for_update_opt RPAREN scoped_statement"""
    p[0] = ('for', p[3], p[5], p[7], p[9])


def p_for_init_opt(p):
    """for_init_opt : for_init
                    | empty"""
    p[0] = p[1]


def p_for_init(p):
    """for_init : type ID
                | type ID ASSIGN expression
                | ID ASSIGN expression"""
    if p[1] in ('int', 'float'):
        var_type = p[1]
        var_name = p[2]
        line = p.lineno(2)
        symbol_table.declare(var_name, var_type, line)
        if len(p) == 3:
            p[0] = ('declaration', var_type, var_name)
        else:
            p[0] = ('block', [
                ('declaration', var_type, var_name),
                ('assignment', var_name, p[4]),
            ])
    else:
        var_name = p[1]
        expr = p[3]
        line = p.lineno(1)
        symbol_table.lookup(var_name, line)
        p[0] = ('assignment', var_name, expr)


def p_for_cond_opt(p):
    """for_cond_opt : expression
                    | empty"""
    p[0] = p[1]


def p_for_update_opt(p):
    """for_update_opt : for_update
                      | empty"""
    p[0] = p[1]


def p_for_update_assign(p):
    """for_update : ID ASSIGN expression"""
    var_name = p[1]
    line = p.lineno(1)
    symbol_table.lookup(var_name, line)
    p[0] = ('assignment', var_name, p[3])


def p_for_update_inc_dec(p):
    """for_update : ID INC
                  | ID DEC"""
    var_name = p[1]
    line = p.lineno(1)
    symbol_table.lookup(var_name, line)
    op = '+' if p[2] == '++' else '-'
    p[0] = ('assignment', var_name, ('binop', op, ('id', var_name), ('number', 1)))

def p_statement_error_recover(p):
    """statement : error SEMICOLON"""
    line = p.lineno(1)
    if line not in syntax_error_lines:
        parser_errors.append(
            f"Line {line}: Invalid statement skipped. Hint: check spelling and statement format before ';'"
        )
        syntax_error_lines.add(line)
    p[0] = None

def p_declaration(p):
    """declaration : type ID SEMICOLON
                   | type ID ASSIGN expression SEMICOLON"""
    var_type = p[1]
    var_name = p[2]
    line = p.lineno(2)

    # Semantic check: declare variable
    symbol_table.declare(var_name, var_type, line)

    if len(p) == 4:
        p[0] = ('declaration', var_type, var_name)
    else:
        # Lower to declaration + assignment for runtime execution compatibility.
        p[0] = ('block', [
            ('declaration', var_type, var_name),
            ('assignment', var_name, p[4]),
        ])

def p_declaration_error(p):
    """declaration : type ID"""
    line = p.lineno(2)
    error_msg = f"Line {line}: Missing ';' after variable declaration"
    _add_error_once(line, error_msg)
    p.parser.errok()
    p[0] = None

def p_type(p):
    """type : INT
            | FLOAT"""
    p[0] = p[1]

def p_assignment(p):
    """assignment : ID ASSIGN expression SEMICOLON"""
    var_name = p[1]
    expr = p[3]
    line = p.lineno(1)
    
    # Semantic check: variable must be declared
    symbol_table.lookup(var_name, line)
    
    p[0] = ('assignment', var_name, expr)

def p_assignment_error_missing_semicolon(p):
    """assignment : ID ASSIGN expression"""
    line = p.lineno(1)
    error_msg = f"Line {line}: Missing ';' after assignment"
    _add_error_once(line, error_msg)
    p.parser.errok()
    p[0] = None

def p_print_stmt_string(p):
    """print_stmt : PRINTF LPAREN STRING RPAREN SEMICOLON
                  | PRINT LPAREN STRING RPAREN SEMICOLON"""
    p[0] = ('print', ('string', p[3]))

def p_print_stmt_expr(p):
    """print_stmt : PRINTF LPAREN expression RPAREN SEMICOLON
                  | PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = ('print', ('expr', p[3]))

def p_print_stmt_printf_format(p):
    """print_stmt : PRINTF LPAREN STRING COMMA expression RPAREN SEMICOLON"""
    p[0] = ('print', ('format_expr', p[3], p[5]))


def p_print_stmt_printf_format_addr(p):
    """print_stmt : PRINTF LPAREN STRING COMMA AMP ID RPAREN SEMICOLON"""
    var_name = p[6]
    line = p.lineno(6)
    symbol_table.lookup(var_name, line)
    p[0] = ('print', ('format_expr', p[3], ('id', var_name)))

def p_print_stmt_error_missing_semicolon(p):
    """print_stmt : PRINTF LPAREN expression RPAREN
                  | PRINT LPAREN expression RPAREN"""
    line = p.lineno(1)
    _add_error_once(line, f"Line {line}: Missing ';' after print statement")
    p.parser.errok()
    p[0] = None


def p_unknown_call_stmt(p):
    """unknown_call_stmt : ID LPAREN call_args_opt RPAREN SEMICOLON"""
    name = p[1]
    line = p.lineno(1)
    suggestion = difflib.get_close_matches(name, ["print", "printf"], n=1, cutoff=0.6)
    if suggestion:
        _add_error_once(
            line,
            f"Line {line}: Unknown function '{name}'. Did you mean '{suggestion[0]}'?"
        )
    else:
        _add_error_once(
            line,
            f"Line {line}: Unknown function '{name}'. Only 'print' and 'printf' are supported"
        )
    p[0] = None


def p_call_args_opt(p):
    """call_args_opt : call_args
                    | empty"""
    p[0] = p[1]


def p_call_args(p):
    """call_args : call_arg
                 | call_args COMMA call_arg"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_call_arg(p):
    """call_arg : expression
                | STRING
                | AMP ID"""
    if len(p) == 3:
        # Treat '&x' as 'x' for lenient C-style compatibility in printf arguments.
        var_name = p[2]
        line = p.lineno(2)
        symbol_table.lookup(var_name, line)
        p[0] = ('id', var_name)
    else:
        p[0] = p[1]

def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = ('number', p[1])

def p_expression_id(p):
    """expression : ID"""
    var_name = p[1]
    line = p.lineno(1)
    
    # Semantic check: variable must be declared
    symbol_table.lookup(var_name, line)
    
    p[0] = ('id', var_name)

def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression"""
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_empty(p):
    """empty :"""
    p[0] = None

# Error handling
def p_error(p):
    global active_parser

    if p:
        line = p.lineno
        if line not in syntax_error_lines:
            error_msg = (
                f"Line {line}: Syntax error near '{p.value}'. "
                "Hint: end each statement with ';' and use valid forms like printf(\"text\");"
            )
            _add_error_once(line, error_msg)

        # Panic-mode recovery: skip tokens until a statement boundary.
        if active_parser is not None:
            while True:
                tok = active_parser.token()
                if tok is None or tok.type in ('SEMICOLON', 'RBRACE'):
                    break
            active_parser.errok()
    else:
        error_msg = "Syntax error at EOF. Hint: check for missing ';' or unmatched '}'"
        _add_error_once(None, error_msg)

# ============================================
# Parser Building
# ============================================

def build_parser():
    """Build and return the parser"""
    parser = yacc.yacc(debug=False, write_tables=False)
    return parser

def parse(code, lexer):
    """
    Parse the code and perform semantic analysis
    Args:
        code: source code string
        lexer: lexer object
    Returns:
        Parsed statement list if successful, None if errors
    """
    global parser_errors, symbol_table, syntax_error_lines, active_parser
    
    # Reset for new parse
    parser_errors = []
    symbol_table = SymbolTable()
    syntax_error_lines = set()
    
    parser = build_parser()
    active_parser = parser
    
    try:
        result = parser.parse(code, lexer=lexer)
        return result
    except Exception as e:
        parser_errors.append(f"Parse error: {str(e)}")
        return None
    finally:
        active_parser = None

def get_errors():
    """Get all errors from parser and symbol table"""
    all_errors = parser_errors + symbol_table.errors
    return all_errors

def get_symbol_table():
    """Get the current symbol table"""
    return symbol_table

# Test the parser
if __name__ == '__main__':
    from lexer import build_lexer
    
    lexer = build_lexer()
    test_code = """
    int a;
    a = 5;
    """
    
    print("Parsing test code...")
    parsed_program = parse(test_code, lexer)
    
    if parsed_program:
        print(f"Parsed program: {parsed_program}")
    
    print("Symbol Table:")
    get_symbol_table().print_table()
    
    errors = get_errors()
    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  {err}")
    else:
        print("\nNo errors found!")
