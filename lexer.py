"""
Lexer for ClearCom - Mini C-like Smart Error Detecting Compiler
Tokenizes the input code and identifies lexical elements
"""

import ply.lex as lex

# List of token names
tokens = (
    'INT',
    'FLOAT',
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'ASSIGN',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
)

# Reserved keywords
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
}

# Token rules (longer patterns first)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Newline tracking for error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Identifier or reserved keyword
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check if it's a reserved word
    return t

# Number (integer or float)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Error handling for invalid characters
def t_error(t):
    error_msg = f"Line {t.lexer.lineno}: Invalid character '{t.value[0]}'"
    print(error_msg)
    t.lexer.errors = getattr(t.lexer, 'errors', [])
    t.lexer.errors.append(error_msg)
    t.lexer.skip(1)

# Build the lexer
def build_lexer():
    """Build and return the lexer"""
    lexer = lex.lex()
    lexer.errors = []
    return lexer

# Test the lexer
if __name__ == '__main__':
    lexer = build_lexer()
    test_input = """
    int a;
    float b;
    a = 5;
    b = 3.14;
    c = a + b;
    """
    
    lexer.input(test_input)
    print("Tokens:")
    for tok in lexer:
        print(f"  {tok.type:10} {tok.value}")
    
    if lexer.errors:
        print("\nErrors found:")
        for err in lexer.errors:
            print(f"  {err}")
