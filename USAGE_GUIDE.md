# 🔧 ClearCom Compiler - Complete Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Usage Modes](#usage-modes)
4. [Supported Syntax](#supported-syntax)
5. [Examples](#examples)
6. [Error Detection](#error-detection)
7. [Syntax Tree (AST)](#syntax-tree-ast)
8. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Step 1: Install PLY
```bash
pip3 install ply
```

Or if you have the project:
```bash
cd Mini-Compiler
pip3 install ply
```

### Verify Installation
```bash
python3 -c "import ply; print('PLY installed successfully!')"
```

---

## Quick Start

### Option 1: Compile from File (Recommended for beginners)
```bash
python3 main.py input.mc
```

### Option 2: Interactive Mode (Type code in terminal)
```bash
python3 interactive.py
```

---

## Usage Modes

### Mode 1️⃣: File-Based Compilation

**Best for:** Programs you want to save and reuse

#### Step 1: Create a .mc file
```bash
cat > myprogram.mc << 'EOF'
int age;
float salary;
age = 25;
salary = 50000 + 5000;
EOF
```

Or use any text editor:
- Visual Studio Code: Create `myprogram.mc`
- nano: `nano myprogram.mc`
- vim: `vim myprogram.mc`

#### Step 2: Compile
```bash
python3 main.py myprogram.mc
```

#### Output will show:
- 📄 Source Code (numbered lines)
- 🔄 Compilation status
- 🌳 Syntax Tree (if successful)
- 📊 Symbol Table
- ✅ or ❌ Compilation result

---

### Mode 2️⃣: Interactive Mode

**Best for:** Learning and testing code quickly

#### Step 1: Start interactive mode
```bash
python3 interactive.py
```

#### Step 2: Write your code line by line
```
  1 > int x;
  2 > x = 10;
  3 > END
```

#### Step 3: View results
- Syntax tree will be displayed
- Symbol table will be shown
- Errors will be reported

#### Interactive Commands
| Command | Description |
|---------|-------------|
| `END` | Compile the code you entered |
| `HELP` | Show syntax help |
| `CLEAR` | Start over with fresh code |
| `QUIT` | Exit the compiler |

---

## Supported Syntax

### 1. Data Types
```c
int x;      // Integer variable
float y;    // Floating-point variable
```

### 2. Variable Declarations
```c
int age;
float pi;
int count;
```

### 3. Assignments
```c
x = 5;
pi = 3.14;
age = 25;
```

### 4. Expressions
```c
result = 10 + 5;           // Addition
result = x - 3;            // Subtraction
total = a * b;             // Multiplication
average = sum / count;     // Division
remainder = x % 2;         // Modulo
```

### 5. Complex Expressions
```c
result = (a + b) * (c - d);
average = (x + y + z) / 3;
```

---

## Examples

### Example 1: Simple Program ✅

**File: simple.mc**
```c
int a;
int b;
a = 10;
b = 20;
```

**Command:**
```bash
python3 main.py simple.mc
```

**Output:**
```
============================================================
           🔧 ClearCom Compiler 🔧
============================================================

📄 Source Code:
------------------------------------------------------------
  1 │ int a;
  2 │ int b;
  3 │ a = 10;
  4 │ b = 20;
------------------------------------------------------------

🔄 Compiling...

🌳 Syntax Tree (AST):
------------------------------------------------------------
📋 PROGRAM
  📝 DECLARATION: a (int)
  📝 DECLARATION: b (int)
  ➡️  ASSIGNMENT: a =
    🔢 NUMBER: 10
  ➡️  ASSIGNMENT: b =
    🔢 NUMBER: 20
------------------------------------------------------------

Symbol Table:
------------------------------
  a               : int
  b               : int
------------------------------

✅ COMPILATION SUCCESSFUL
============================================================
No errors found! Code is valid.
============================================================
```

### Example 2: Using Interactive Mode

**Command:**
```bash
python3 interactive.py
```

**Session:**
```
============================================================
         🔧 ClearCom Interactive Compiler 🔧
============================================================

📝 Commands:
  • Type your code line by line
  • Type 'END' to finish (on new line)
  • Type 'HELP' for syntax help
  • Type 'CLEAR' to start over
  • Type 'QUIT' to exit

------------------------------------------------------------

Enter your code (type 'END' on a new line to compile):
Type 'HELP' for help, 'CLEAR' to reset, 'QUIT' to exit

  1 > int x;
  2 > float y;
  3 > x = 5;
  4 > y = 3.14;
  5 > END

------------------------------------------------------------
📊 COMPILATION REPORT
------------------------------------------------------------

📄 Source Code:
----------------------------------------
  1 │ int x;
  2 │ float y;
  3 │ x = 5;
  4 │ y = 3.14;
----------------------------------------

🔄 Compiling...

🌳 Syntax Tree (AST):
----------------------------------------
📋 PROGRAM
  📝 DECLARATION: x (int)
  📝 DECLARATION: y (float)
  ➡️  ASSIGNMENT: x =
    🔢 NUMBER: 5
  ➡️  ASSIGNMENT: y =
    🔢 NUMBER: 3.14
----------------------------------------

Symbol Table:
------------------------------
  x               : int
  y               : float
------------------------------

✅ COMPILATION SUCCESSFUL
============================================================
No errors found! Code is valid.
============================================================
```

### Example 3: Program with Expressions

**File: math.mc**
```c
int a;
int b;
int sum;
a = 100;
b = 50;
sum = a + b;
```

**Command:**
```bash
python3 main.py math.mc
```

---

## Error Detection

### Error Types Detected

#### 1. Missing Semicolon
```c
int x      // ❌ Missing ;
x = 5;
```
**Error:** `Line 1: Missing ';' after variable declaration`

#### 2. Undeclared Variable
```c
x = 10;    // ❌ x not declared
```
**Error:** `Line 1: Undeclared variable 'x'`

#### 3. Duplicate Declaration
```c
int x;
int x;     // ❌ x already declared
```
**Error:** `Line 2: Duplicate variable 'x' (previously declared)`

#### 4. Invalid Character
```c
int a$;    // ❌ $ is invalid
```
**Error:** `Line 1: Invalid character '$'`

#### 5. Syntax Error
```c
x = ;      // ❌ No value
```
**Error:** `Line 1: Syntax error at ';'`

### Running with Errors

**File: errors.mc**
```c
int a
a = 10;
b = 5;
int a;
```

**Command:**
```bash
python3 main.py errors.mc
```

**Output:**
```
❌ COMPILATION FAILED
============================================================
Total Errors: 3

  1. ✗ Line 1: Missing ';' after variable declaration
  2. ✗ Line 2: Undeclared variable 'b'
  3. ✗ Line 3: Duplicate variable 'a' (previously declared)
============================================================
```

---

## Syntax Tree (AST)

The compiler shows the **Abstract Syntax Tree** which represents your code structure.

### Tree Symbols
| Symbol | Meaning |
|--------|---------|
| 📋 | Program root |
| 📝 | Variable declaration |
| ➡️ | Variable assignment |
| ⚙️ | Operator/operation |
| 🔢 | Number literal |
| 🔤 | Variable reference |

### Example Tree
```
📋 PROGRAM
  📝 DECLARATION: x (int)
  📝 DECLARATION: y (float)
  ➡️  ASSIGNMENT: sum =
    ⚙️  OPERATOR: +
      🔤 VARIABLE: x
      🔂 NUMBER: 5
```

This shows:
- Declare x as int
- Declare y as float
- Assign to sum: x + 5

---

## Troubleshooting

### Problem: "pip: command not found"
**Solution:**
```bash
# Use python3 directly
python3 -m pip install ply
```

### Problem: "Module not found: ply"
**Solution:**
```bash
# Reinstall PLY
python3 -m pip install --upgrade ply
```

### Problem: "File not found"
**Solution:**
```bash
# Make sure you're in the correct directory
cd Mini-Compiler
ls *.mc           # Check if file exists

# Or use full path
python3 main.py /full/path/to/file.mc
```

### Problem: "python3: command not found"
**Solution (macOS):**
```bash
# Install Python 3
brew install python@3.11
```

**Solution (Ubuntu/Debian):**
```bash
sudo apt-get install python3
```

### Problem: "Syntax error" but code looks correct
**Solution:**
- Check for missing semicolons (`;`)
- Check for typos in variable names
- Make sure variables are declared before use
- Make sure variable names start with letter or underscore

### Problem: Parser creates strange files
**Solution:**
```bash
# Clean up generated files
rm -f parser.out parsetab.py
```

---

## Project Files Reference

| File | Purpose |
|------|---------|
| `main.py` | File-based compiler entry point |
| `interactive.py` | Interactive mode (REPL) |
| `lexer.py` | Tokenizer (splits code into tokens) |
| `parser.py` | Parser (validates grammar & builds AST) |
| `symbol_table.py` | Variable management |
| `input.mc` | Sample valid code |
| `error_input.mc` | Sample code with errors |
| `error_test2.mc` | More error examples |

---

## Quick Reference

```bash
# Install dependencies
pip3 install ply

# Compile a file
python3 main.py mycode.mc

# Interactive mode
python3 interactive.py

# Create a test file
echo "int x;" > test.mc
echo "x = 42;" >> test.mc

# Compile test file
python3 main.py test.mc
```

---

## Tips for Learning

1. **Start simple:** Create basic programs first
2. **Use interactive mode:** Experiment with syntax
3. **Watch the AST:** See how code is structured
4. **Check the symbol table:** Track your variables
5. **Read error messages:** They tell you exactly what's wrong
6. **Extend it:** Add more features as you learn

---

## Support

For issues or questions:
1. Check the error message (it's usually helpful!)
2. Review the examples in this guide
3. Look at the sample files (input.mc, error_input.mc)
4. Review the code comments in Python files

Happy coding! 🚀
