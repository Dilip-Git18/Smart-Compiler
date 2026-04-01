"""
Parser for ClearCom - Mini C-like Smart Error Detecting Compiler
Performs syntax analysis and semantic checking using PLY
"""

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
                 | print_stmt"""
    p[0] = p[1]

def p_statement_error_recover(p):
    """statement : error SEMICOLON"""
    line = p.lineno(1)
    parser_errors.append(f"Line {line}: Invalid statement skipped")
    p[0] = None

def p_declaration(p):
    """declaration : type ID SEMICOLON"""
    var_type = p[1]
    var_name = p[2]
    line = p.lineno(2)
    
    # Semantic check: declare variable
    symbol_table.declare(var_name, var_type, line)
    
    p[0] = ('declaration', var_type, var_name)

def p_declaration_error(p):
    """declaration : type ID"""
    line = p.lineno(2)
    error_msg = f"Line {line}: Missing ';' after variable declaration"
    parser_errors.append(error_msg)
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
    parser_errors.append(error_msg)
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

def p_print_stmt_error_missing_semicolon(p):
    """print_stmt : PRINTF LPAREN expression RPAREN
                  | PRINT LPAREN expression RPAREN"""
    line = p.lineno(1)
    parser_errors.append(f"Line {line}: Missing ';' after print statement")
    p[0] = None

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
                  | expression MODULO expression"""
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]

# Error handling
def p_error(p):
    if p:
        error_msg = f"Line {p.lineno}: Syntax error at '{p.value}'"
        parser_errors.append(error_msg)
        # Allow parser to continue and build partial parse results when possible.
        yacc.errok()
    else:
        error_msg = "Syntax error at EOF"
        parser_errors.append(error_msg)

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
    global parser_errors, symbol_table
    
    # Reset for new parse
    parser_errors = []
    symbol_table = SymbolTable()
    
    parser = build_parser()
    
    try:
        result = parser.parse(code, lexer=lexer)
        return result
    except Exception as e:
        parser_errors.append(f"Parse error: {str(e)}")
        return None

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
