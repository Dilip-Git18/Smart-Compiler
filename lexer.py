"""
Lexer for ClearCom - Mini C-like Smart Error Detecting Compiler
Tokenizes the input code and identifies lexical elements.
"""

try:
    import ply.lex as lex
except ImportError as exc:
    raise ImportError(
        "PLY is not installed in the selected Python environment. "
        "Install it with: python3 -m pip install ply"
    ) from exc

# List of token names (only tokens actually used in the language)
tokens = (
    'INT',
    'FLOAT',
    'MAIN',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'PRINTF',
    'PRINT',
    'ID',
    'STRING',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'LT',
    'LE',
    'GT',
    'GE',
    'EQ',
    'NE',
    'INC',
    'DEC',
    'ASSIGN',
    'SEMICOLON',
    'COMMA',
    'AMP',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
)

# Reserved keywords
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'main': 'MAIN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'printf': 'PRINTF',
    'print': 'PRINT',
}

# Token rules (longer patterns first)
t_INC = r'\+\+'
t_DEC = r'--'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LT = r'<'
t_GT = r'>'
t_ASSIGN = r'='
t_SEMICOLON = r';'
t_COMMA = r','
t_AMP = r'&'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Newline tracking for error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore C preprocessor lines like #include <stdio.h>
def t_preprocessor(t):
    r'\#[^\n]*'
    pass

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

# Double-quoted string literal used by printf
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t

# Error handling for invalid characters
def t_error(t):
    line_no = t.lexer.lineno
    line_errors = getattr(t.lexer, "line_errors", set())

    # Report only once per line to avoid noisy cascaded errors.
    if line_no not in line_errors:
        ch = t.value[0]
        error_msg = (
            f"Line {line_no}: Unsupported character '{ch}'. "
            "ClearCom supports only declarations, assignments, and expressions."
        )
        t.lexer.errors.append(error_msg)
        line_errors.add(line_no)
        t.lexer.line_errors = line_errors

    # Skip the rest of the current line to avoid one error per character.
    newline_pos = t.value.find("\n")
    if newline_pos == -1:
        t.lexer.skip(len(t.value))
    else:
        t.lexer.skip(newline_pos)

# Build the lexer
def build_lexer():
    """Build and return the lexer"""
    lexer = lex.lex()
    lexer.errors = []
    lexer.line_errors = set()
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
