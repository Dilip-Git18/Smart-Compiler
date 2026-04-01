# ClearCom - Quick Start Guide

## 1. Install Dependencies
```bash
python3 -m pip install ply
```

## 2. Run the Compiler
```bash
# Compile a file
python3 main.py input.mc

# Or test with errors
python3 main.py error_input.mc
```

## 3. Create Your Own File

Create a file with `.mc` extension:

```bash
# Create a new file
cat > myprogram.mc << 'EOF'
int age;
float salary;
age = 25;
salary = 50000 + 5000;
EOF

# Compile it
python3 main.py myprogram.mc
```

## 4. Supported Syntax

### Variable Declaration
```c
int x;
float y;
```

### Assignment
```c
x = 10;
y = 3.14;
y = x + 5;
```

### Expressions
```c
int result;
result = 10 + 5;
result = a + b;
```

## 5. Error Types Detected

| Error | Example |
|-------|---------|
| Missing semicolon | `int a` (missing `;`) |
| Undeclared variable | `x = 5;` (if `x` not declared) |
| Duplicate declaration | `int a; int a;` |
| Invalid character | `int a$;` |

## 6. Example Outputs

### Success ✓
```
COMPILATION SUCCESSFUL
--------------------------------------------------
No errors found!
--------------------------------------------------
```

### Failure ✗
```
COMPILATION FAILED
--------------------------------------------------
Errors:
  ✗ Line 1: Missing ';' after variable declaration
  ✗ Line 3: Undeclared variable 'x'
--------------------------------------------------
```

## 7. Project Files

- `lexer.py` - Tokenization
- `parser.py` - Syntax analysis
- `symbol_table.py` - Variable tracking
- `main.py` - Entry point
- `input.mc` - Good example
- `error_input.mc` - Error example
- `error_test2.mc` - More errors example

Enjoy! 🚀
