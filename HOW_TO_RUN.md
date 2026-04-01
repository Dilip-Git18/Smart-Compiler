# ⚡ HOW TO RUN - ClearCom Compiler

## 🎯 The Fastest Way to Get Started

### Step 1: Install (one time only)
```bash
pip3 install ply
```

### Step 2: Run (choose one)

**Option A: Compile a saved file**
```bash
python3 main.py input.mc
```

**Option B: Type code interactively**  
```bash
python3 interactive.py
```

---

## 🔄 Complete Step-by-Step Guide

### Method 1️⃣: Compile an Existing File

```bash
cd /path/to/Mini-Compiler
python3 main.py input.mc
```

**What happens:**
- Code is read from `input.mc`
- Lexer tokenizes it
- Parser builds syntax tree
- Errors are checked
- Results are displayed

**Output includes:**
- 📄 Source code (line by line)
- 🌳 Syntax tree visualization
- 📊 Symbol table
- ✅ Success or ❌ Failure

---

### Method 2️⃣: Create & Compile Your Own File

#### Step 1: Create a file
```bash
cat > mycode.mc << 'EOF'
int count;
float average;
count = 10;
average = 9.5;
EOF
```

#### Step 2: Compile it
```bash
python3 main.py mycode.mc
```

#### Step 3: See results
Results show immediately in terminal

---

### Method 3️⃣: Interactive Mode (No Files Needed!)

#### Start the compiler:
```bash
python3 interactive.py
```

#### Type your code:
```
  1 > int x;
  2 > x = 42;
  3 > END
```

#### Special commands:
- `END` → Compile
- `HELP` → Show syntax help
- `CLEAR` → Start over
- `QUIT` → Exit

#### After compilation:
- You'll see the syntax tree
- You'll see the symbol table
- Then it asks: "Compile more code? (yes/no):"
- Type `yes` to write more or `no` to exit

---

## 📝 Sample Files Included

### Test with good code:
```bash
python3 main.py input.mc
```

### Test with errors:
```bash
# Shows 3 errors
python3 main.py error_input.mc

# Shows 3 different errors
python3 main.py error_test2.mc
```

---

## 📊 Full Example Session

### Terminal session:
```bash
$ python3 main.py input.mc
============================================================
           🔧 ClearCom Compiler 🔧
============================================================

📄 Source Code:
  1 │ int a;
  2 │ float b;
  3 │ a = 5;
  4 │ b = 3 + 2;

🌳 Syntax Tree (AST):
📋 PROGRAM
  📝 DECLARATION: a (int)
  📝 DECLARATION: b (float)
  ➡️  ASSIGNMENT: a =
    🔢 NUMBER: 5
  ➡️  ASSIGNMENT: b =
    ⚙️  OPERATOR: +
      🔢 NUMBER: 3
      🔢 NUMBER: 2

Symbol Table:
  a               : int
  b               : float

✅ COMPILATION SUCCESSFUL
============================================================
```

---

## 🎓 Learning Activities

### Activity 1: See it work
```bash
python3 main.py input.mc
```

### Activity 2: Find errors
```bash
python3 main.py error_test2.mc
# Count how many errors it finds
```

### Activity 3: Write your own
```bash
# Create new file
cat > lesson1.mc << 'EOF'
int age;
int height;
age = 25;
height = 180;
EOF

# Compile it
python3 main.py lesson1.mc
```

### Activity 4: Interactive exploration
```bash
python3 interactive.py

# Type:
# int x;
# int y;
# x = 10;
# y = 20;
# END

# Then experiment more!
```

---

## 🖱️ Command Reference

| What you want | Command |
|---|---|
| Install PLY | `pip3 install ply` |
| Compile file | `python3 main.py filename.mc` |
| Interactive | `python3 interactive.py` |
| Create file | `cat > file.mc << 'EOF'` + code + `EOF` |
| List files | `ls -la` |
| Clean temp files | `rm -f parser.out parsetab.py *.pyc` |
| Check Python | `python3 --version` |
| Check PLY | `python3 -c "import ply; print('OK')"` |

---

## 🔍 Checking Installation

```bash
# Check 1: Python installed?
python3 --version
# Should show: Python 3.x.x

# Check 2: PLY installed?
python3 -c "import ply; print('PLY OK')"
# Should show: PLY OK

# Check 3: Files exist?
ls *.py *.mc
# Should show: lexer.py, parser.py, main.py, etc

# Check 4: Try compiling
python3 main.py input.mc
# Should show: ✅ COMPILATION SUCCESSFUL
```

---

## ❌ If Something Goes Wrong

### Problem: "pip not found"
```bash
python3 -m pip install ply
```

### Problem: "ply not found"
```bash
pip3 install --upgrade ply
```

### Problem: "File not found"
```bash
# Check current directory
pwd
ls

# Make sure you're in the right directory
cd /path/to/Mini-Compiler
```

### Problem: Weird error
```bash
# Clean up and try again
rm -f parser.out parsetab.py
python3 main.py input.mc
```

---

## 🚀 Three Ways to Learn

### Way 1: File Mode (Recommended for beginners)
```bash
python3 main.py input.mc
```
- See complete output
- Can save your code
- Good for testing

### Way 2: Interactive Mode (For learning)
```bash
python3 interactive.py
```
- Immediate feedback
- No file needed
- Great for experimenting

### Way 3: Create & Test (For practice)
```bash
# Create file
cat > test.mc << 'EOF'
int x;
x = 100;
EOF

# Compile
python3 main.py test.mc
```
- Combines benefits of both
- Can reuse code easily

---

## 📖 Documentation Files

| File | What to Read |
|------|---|
| `HOW_TO_RUN.md` | **← YOU ARE HERE** - Running commands |
| `BEGINNER_GUIDE.md` | Learning the basics |
| `USAGE_GUIDE.md` | Detailed guide with examples |
| `QUICKSTART.md` | Quick reference |
| `README.md` | Project overview |

---

## 🎯 Your First Programs

### Program 1: Hello Variables
```c
int a;
int b;
a = 10;
b = 20;
```

### Program 2: Math Time
```c
int x;
int y;
int sum;
x = 5;
y = 3;
sum = x + y;
```

### Program 3: Different types
```c
int count;
float price;
count = 100;
price = 99.99;
```

---

## ✨ Next Steps

1. **Try it now:** `python3 main.py input.mc`
2. **Experiment:** `python3 interactive.py`
3. **Read guide:** `BEGINNER_GUIDE.md`
4. **Write code:** Create your own `.mc` files
5. **Explore:** Look at the Python source files

---

**That's all you need! You're ready to go! 🚀**
