# 📖 ClearCom - Complete Compiler Guide

## What is ClearCom?

**ClearCom** is a mini compiler that reads C-like code and analyzes it. It has:
- ✅ A **Lexer** that breaks code into tokens
- ✅ A **Parser** that checks grammar  
- ✅ An **AST** (Abstract Syntax Tree) that shows code structure
- ✅ A **Symbol Table** that tracks variables
- ✅ **Error Detection** that finds mistakes

---

## 🚀 Getting Started in 3 Steps

### Step 1: Install PLY
```bash
pip3 install ply
```

### Step 2: Choose Your Mode

**Option A - File Mode (Save your code)**
```bash
python3 main.py input.mc
```

**Option B - Interactive Mode (Type in terminal)**
```bash
python3 interactive.py
```

### Step 3: View Results
- 📋 Source code lines
- 🌳 Syntax tree (AST)
- 📊 Symbol table
- ✅ Compilation status

---

## 📝 How to Create Your First Program

### Using File Mode

**Create a file called `myprogram.mc`:**
```bash
cat > myprogram.mc << 'EOF'
int age;
float salary;
age = 25;
salary = 50000 + 5000;
EOF
```

**Compile it:**
```bash
python3 main.py myprogram.mc
```

**You'll see:**
```
========================================
📄 Source Code:
  1 │ int age;
  2 │ float salary;
  3 │ age = 25;
  4 │ salary = 50000 + 5000;

🌳 Syntax Tree (AST):
📋 PROGRAM
  📝 DECLARATION: age (int)
  📝 DECLARATION: salary (float)
  ➡️  ASSIGNMENT: age =
    🔢 NUMBER: 25
  ➡️  ASSIGNMENT: salary =
    ⚙️  OPERATOR: +
      🔢 NUMBER: 50000
      🔢 NUMBER: 5000

✅ COMPILATION SUCCESSFUL
========================================
```

---

## 🖥️ Interactive Mode Step-by-Step

### Start Interactive Mode
```bash
python3 interactive.py
```

### Type Your Code
```
  1 > int x;
  2 > x = 42;
  3 > END
```

### See Your Results
- 🌳 Syntax tree appears
- 📊 Symbol table shows `x : int`
- ✅ Compilation result
- Ask "Compile more? (yes/no):"
  - Type `yes` to write more code
  - Type `no` to exit

### Interactive Commands
| What to Type | What It Does |
|---|---|
| `int x;` | Declare integer x |
| `x = 10;` | Assign value 10 to x |
| `END` | Compile the code you wrote |
| `HELP` | Show syntax help |
| `CLEAR` | Start over with new code |
| `QUIT` | Exit the compiler |

---

## 💻 Language You Can Use

### Variables (Declaration)
```c
int count;     // Integer variable
float price;   // Decimal number variable
```

### Assignment (Give values)
```c
count = 5;
price = 19.99;
```

### Expressions (Math)
```c
sum = 10 + 5;          // Add: 10 + 5 = 15
difference = 20 - 3;   // Subtract: 20 - 3 = 17
product = 4 * 5;       // Multiply: 4 * 5 = 20
quotient = 20 / 4;     // Divide: 20 / 4 = 5
remainder = 10 % 3;    // Modulo: 10 % 3 = 1
```

### Complex Math
```c
result = (10 + 5) * 2;    // (10 + 5) = 15, then 15 * 2 = 30
average = (a + b + c) / 3;
```

---

## ✅ Program Examples

### Example 1: Simple (✓ Works)
```c
int a;
int b;
a = 10;
b = 20;
```

### Example 2: With Math (✓ Works)
```c
int x;
int y;
int sum;
x = 100;
y = 50;
sum = x + y;
```

### Example 3: Mixed Types (✓ Works)
```c
int count;
float average;
count = 10;
average = 9.5;
```

---

## ❌ Common Errors & How to Fix Them

### Error 1: Missing Semicolon
```c
❌ int x        // Missing ;
✅ int x;      // Fixed
```
**Compiler says:** `Line 1: Missing ';' after variable declaration`

### Error 2: Variable Not Declared
```c
❌ x = 5;       // x not declared first!
✅ int x;       // Declare first
   x = 5;       // Then use
```
**Compiler says:** `Line 1: Undeclared variable 'x'`

### Error 3: Duplicate Declaration
```c
❌ int x;
   int x;       // Can't declare x twice!
   
✅ int x;       // Only declare once
   x = 5;       // Use it multiple times
   x = 10;
```
**Compiler says:** `Line 2: Duplicate variable 'x'`

### Error 4: Invalid Character
```c
❌ int a$;      // $ is invalid
✅ int a;       // Only use letters, numbers, _
```
**Compiler says:** `Line 1: Invalid character '$'`

---

## 🌳 Understanding the Syntax Tree

The compiler shows a **tree** of how it understood your code.

### Symbols Used
- 📋 = Whole program
- 📝 = Variable declaration
- ➡️ = Variable assignment
- ⚙️ = Math operation (+, -, *, /)
- 🔢 = A number (5, 42, 3.14, etc)
- 🔤 = A variable name

### Example Tree
```
📋 PROGRAM
  📝 DECLARATION: x (int)
  ➡️  ASSIGNMENT: x =
    ⚙️  OPERATOR: +
      🔢 NUMBER: 5
      🔢 NUMBER: 3
```

**Meaning:** "Declare x as integer, then assign to x the result of 5 + 3"

---

## 🎓 Learning Compiler Basics

This compiler teaches how real compilers work:

1. **Lexer** - Breaks code into pieces (tokens)
   - Finds keywords: `int`, `float`
   - Finds operators: `+`, `-`, `*`, `/`, `=`
   - Finds numbers and variable names
   - Finds special characters: `;`, `(`, `)`

2. **Parser** - Checks if the pieces make sense
   - Makes sure declarations have `;`
   - Makes sure assignments have `;`
   - Creates a tree showing the structure

3. **Symbol Table** - Remembers variable info
   - `x: int` means "x is an integer"
   - Checks if variables are used before declared
   - Checks if variables are declared twice

4. **Semantic Analyzer** - Checks for logic errors
   - Can't use `y` if you didn't declare it
   - Can't declare `x` twice
   - Must have `;` at end of statements

---

## 📂 Project Files & What They Do

| File | Does What |
|------|-----------|
| `lexer.py` | Breaks code into tokens |
| `parser.py` | Checks grammar, builds tree |
| `symbol_table.py` | Tracks variables |
| `main.py` | Reads `.mc` file, runs compiler |
| `interactive.py` | Interactive terminal compiler |
| `input.mc` | Example: good code |
| `error_input.mc` | Example: bad code |
| `error_test2.mc` | Example: more errors |

---

## 🔧 Terminal Commands Reference

### Compile a file:
```bash
python3 main.py mycode.mc
```

### Run interactive mode:
```bash
python3 interactive.py
```

### Create a test file:
```bash
echo "int x;" > test.mc
echo "x = 42;" >> test.mc
```

### Compile and see result:
```bash
python3 main.py test.mc
```

### Clean up (removes temp files):
```bash
rm -f parser.out parsetab.py *.pyc
```

---

## 🆘 Troubleshooting

### Problem: "pip3 not found"
```bash
# Use python3 directly
python3 -m pip install ply
```

### Problem: "No module named 'ply'"
```bash
# Reinstall
pip3 install --upgrade ply
```

### Problem: "File not found"
```bash
# Check current directory
pwd
ls *.mc

# Or use full path
python3 main.py /Users/yourname/file.mc
```

### Problem: python3 command doesn't work
**macOS:**
```bash
brew install python@3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3
```

### Problem: Weird error about parser
```bash
# Clean and try again
rm -f parser.out parsetab.py
python3 main.py input.mc
```

---

## 💡 Fun Things to Try

### Try 1: Create your own program
```bash
cat > mymath.mc << 'EOF'
int a;
int b;
int result;
a = 50;
b = 30;
result = a + b;
EOF

python3 main.py mymath.mc
```

### Try 2: Find errors
```bash
# This file has errors, find them:
cat > broken.mc << 'EOF'
int x
x = 5;
y = x + 10;
int x;
EOF

python3 main.py broken.mc
```
**Errors:** missing `;`, undeclared `y`, duplicate `x`

### Try 3: Interactive practice
```bash
python3 interactive.py

# Type:
# int count;
# count = 1 + 2 + 3;
# END
```

### Try 4: Explore files
Read the code files to see:
- How `lexer.py` tokenizes
- How `parser.py` builds trees
- How errors are found

---

## 🎯 Next Learning Steps

1. **Understand the flow:**
   - Code → Lexer → Parser → Symbol Table → Output

2. **Read the source files:**
   - Look at comments in the Python files

3. **Modify and experiment:**
   - Change error messages
   - Add new operators
   - Try adding new keywords

4. **Extend the language:**
   - Add `if-else` statements
   - Add `while` loops
   - Add function support

5. **Study theory:**
   - Context-free grammar
   - Abstract syntax trees
   - Type systems

---

## 📞 Get Help

1. **Read error messages** - They tell you what's wrong!
2. **See the samples** - `input.mc`, `error_input.mc`, `error_test2.mc`
3. **Use HELP in interactive** - Type `HELP` to see syntax
4. **Check the guides** - `README.md`, `USAGE_GUIDE.md`

---

## 🎓 Key Concepts

| Term | Meaning |
|------|---------|
| **Lexer** | Breaks code into tokens |
| **Parser** | Checks grammar, builds tree |
| **AST** | Tree showing code structure |
| **Token** | A piece of code (keyword, number, etc) |
| **Symbol Table** | Database of variables |
| **Semantic** | Checking meaning, not just grammar |
| **Compile** | Turn code into something usable |

---

## 🚀 Ready to Start?

**Try this right now:**
```bash
# Install
pip3 install ply

# See it work
python3 main.py input.mc

# Try interactive
python3 interactive.py
```

**That's it! You're using a compiler! 🎉**

---

**Enjoy learning! The compiler inside your computer uses these same ideas! 💻✨**
