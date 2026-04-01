# ⚡ ClearCom - Quick Reference Card

## 🚀 30-Second Start

```bash
pip3 install ply        # Install (once)
python3 main.py input.mc  # Run file mode
python3 interactive.py    # Run interactive
```

---

## 📋 Two Ways to Use

### File Mode
```bash
python3 main.py mycode.mc
```
Output shows: 📄 Code | 🌳 Tree | 📊 Table | ✅ Status

### Interactive Mode  
```bash
python3 interactive.py
```
Type code → END → See results → Repeat

---

## 💻 Supported Syntax

```c
int x;              // Declare integer
float y;            // Declare float
x = 5;              // Assign value
y = 3.14;           // Decimal assignment
z = a + b;          // Addition
result = 10 - 3;    // Subtraction
product = 2 * 3;    // Multiplication
division = 20 / 4;  // Division
mod = 10 % 3;       // Modulo (remainder)
```

---

## 🌳 Syntax Tree Symbols

| Symbol | Meaning |
|--------|---------|
| 📋 | Program |
| 📝 | Declaration |
| ➡️ | Assignment |
| ⚙️ | Operator |
| 🔢 | Number |
| 🔤 | Variable |

---

## ❌ Common Errors

| Error | Fix |
|-------|-----|
| Missing `;` | Add semicolon: `int x;` |
| Undeclared var | Declare first: `int x; x = 5;` |
| Duplicate var | Don't declare twice |
| Invalid char | Use only: letters, numbers, _ |

---

## 📖 Documentation Map

| File | Purpose |
|------|---------|
| **HOW_TO_RUN.md** | ← START HERE |
| BEGINNER_GUIDE.md | Learning |
| USAGE_GUIDE.md | Complete guide |
| QUICKSTART.md | Commands |
| BUILD_SUMMARY.md | What was built |

---

## 📂 Files You Have

### Compiler (5 files)
- `lexer.py` - Tokenizer
- `parser.py` - Parser + AST
- `symbol_table.py` - Variables
- `main.py` - File mode
- `interactive.py` - Terminal mode

### Docs (7 files)
- `HOW_TO_RUN.md` ⭐
- `BEGINNER_GUIDE.md`
- `USAGE_GUIDE.md`
- `QUICKSTART.md`
- `README.md`
- `BUILD_SUMMARY.md`
- `DOCUMENTATION_INDEX.md`

### Examples (3 files)
- `input.mc` - Good code
- `error_input.mc` - Bad code 1
- `error_test2.mc` - Bad code 2

---

## 🎯 Quick Tasks

### Create a file
```bash
cat > test.mc << 'EOF'
int x;
x = 42;
EOF
```

### Compile it
```bash
python3 main.py test.mc
```

### Fix parser cache
```bash
rm -f parser.out parsetab.py
```

### Check setup
```bash
python3 -c "import ply; print('OK')"
```

---

## 💡 Try These Examples

### Example 1 (Simple)
```bash
python3 main.py input.mc
```

### Example 2 (Errors)
```bash
python3 main.py error_test2.mc
```

### Example 3 (Interactive)
```bash
python3 interactive.py
# Type:
# int x;
# x = 10;
# END
```

---

## 🔧 Troubleshooting

### PLY not found
```bash
pip3 install ply
```

### File not found
```bash
ls input.mc
cd /path/to/project
```

### Python error
```bash
python3 main.py input.mc
# or
python3 interactive.py
```

---

## 📊 What Happens

```
Your Code
    ↓
Lexer (Tokenize)
    ↓
Parser (Check Grammar → Build Tree)
    ↓
Symbol Table (Validate Variables)
    ↓
Output (Show Results)
```

---

## ✨ Features

- ✅ Lexer/Tokenizer
- ✅ Parser with AST
- ✅ Syntax tree visualization  
- ✅ Symbol table tracking
- ✅ Error detection
- ✅ 2 modes (file + interactive)

---

## 📱 Most Common Commands

```bash
# Check installation
pip3 install ply

# See it work
python3 main.py input.mc

# Play interactively
python3 interactive.py

# Create your own code
cat > mycode.mc << 'EOF'
int a;
a = 100;
EOF

# Compile yours
python3 main.py mycode.mc
```

---

**Start now: `python3 main.py input.mc` 🚀**

Then read: `HOW_TO_RUN.md`
