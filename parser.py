"""
Parser for ClearCom - Mini C-like Smart Error Detecting Compiler
Performs syntax analysis and semantic checking using PLY
"""

import ply.yacc as yacc
from lexer import tokens  # Import tokens from lexer
from symbol_table import SymbolTable

# Symbol table for semantic analysis
symbol_table = SymbolTable()

# Parser error tracking
parser_errors = []

# ============================================
# AST Node Classes
# ============================================

class ASTNode:
    """Base AST node for syntax tree"""
    def __init__(self, node_type):
        self.type = node_type
        self.children = []
    
    def add_child(self, child):
        if child is not None:
            self.children.append(child)
    
    def print_tree(self, indent=0):
        """Print the AST in a tree format"""
        prefix = "  " * indent
        if self.type == 'program':
            print(f"{prefix}📋 PROGRAM")
        elif self.type == 'declaration':
            print(f"{prefix}📝 DECLARATION: {self.children[1]} ({self.children[0]})")
        elif self.type == 'assignment':
            print(f"{prefix}➡️  ASSIGNMENT: {self.children[0]} =")
            for i, child in enumerate(self.children[1:], 1):
                if hasattr(child, 'print_tree'):
                    child.print_tree(indent + 1)
        elif self.type == 'binop':
            print(f"{prefix}⚙️  OPERATOR: {self.children[0]}")
            for child in self.children[1:]:
                if hasattr(child, 'print_tree'):
                    child.print_tree(indent + 1)
        elif self.type == 'number':
            print(f"{prefix}🔢 NUMBER: {self.children[0]}")
        elif self.type == 'id':
            print(f"{prefix}🔤 VARIABLE: {self.children[0]}")
        
        # For program node, print children
        if self.type == 'program':
            for child in self.children:
                if hasattr(child, 'print_tree'):
                    child.print_tree(indent + 1)

# ============================================
# Grammar Rules
# ============================================

def p_program(p):
    """program : statement_list"""
    node = ASTNode('program')
    for stmt in p[1]:
        if stmt:
            node.add_child(stmt)
    p[0] = node

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
                 | assignment"""
    p[0] = p[1]

def p_declaration(p):
    """declaration : type ID SEMICOLON"""
    var_type = p[1]
    var_name = p[2]
    line = p.lineno(2)
    
    # Semantic check: declare variable
    symbol_table.declare(var_name, var_type, line)
    
    node = ASTNode('declaration')
    node.add_child(var_type)
    node.add_child(var_name)
    p[0] = node

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
    var_type = symbol_table.lookup(var_name, line)
    
    node = ASTNode('assignment')
    node.add_child(var_name)
    node.add_child(expr)
    p[0] = node

def p_assignment_error_missing_semicolon(p):
    """assignment : ID ASSIGN expression"""
    line = p.lineno(1)
    error_msg = f"Line {line}: Missing ';' after assignment"
    parser_errors.append(error_msg)
    p[0] = None

def p_expression_number(p):
    """expression : NUMBER"""
    node = ASTNode('number')
    node.add_child(p[1])
    p[0] = node

def p_expression_id(p):
    """expression : ID"""
    var_name = p[1]
    line = p.lineno(1)
    
    # Semantic check: variable must be declared
    symbol_table.lookup(var_name, line)
    
    node = ASTNode('id')
    node.add_child(var_name)
    p[0] = node

def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression"""
    node = ASTNode('binop')
    node.add_child(p[2])
    node.add_child(p[1])
    node.add_child(p[3])
    p[0] = node

def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]

# Error handling
def p_error(p):
    if p:
        error_msg = f"Line {p.lineno}: Syntax error at '{p.value}'"
        parser_errors.append(error_msg)
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
        AST if successful, None if errors
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
    ast = parse(test_code, lexer)
    
    if ast:
        print(f"AST: {ast}")
    
    print("Symbol Table:")
    get_symbol_table().print_table()
    
    errors = get_errors()
    if errors:
        print("\nErrors:")
        for err in errors:
            print(f"  {err}")
    else:
        print("\nNo errors found!")
