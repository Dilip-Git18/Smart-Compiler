# 📚 ClearCom Compiler - Documentation Index

Welcome to **ClearCom** - A Mini C-like Smart Error Detecting Compiler!

This document helps you find the right guide for your needs.

---

## 🎯 Find What You Need

### "I just want to run it NOW!"
→ Read: [HOW_TO_RUN.md](HOW_TO_RUN.md)

**Quick command:**
```bash
pip3 install ply
python3 main.py input.mc
```

---

### "I'm a complete beginner"
→ Read: [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)

Learn:
- What is a compiler?
- Simple language syntax
- How to use the tool
- Common errors
- Understanding syntax trees

---

### "I want to learn and see examples"
→ Read: [USAGE_GUIDE.md](USAGE_GUIDE.md)

Includes:
- Installation steps
- Complete syntax reference
- Detailed examples
- Error detection guide
- All commands explained

---

### "I need quick reference"
→ Read: [QUICKSTART.md](QUICKSTART.md)

Get:
- Quick commands
- Syntax reference
- Common tasks
- File structure

---

### "I want project overview"
→ Read: [README.md](README.md)

Contains:
- Feature list
- Project structure
- Learning points
- Troubleshooting

---

## 📖 All Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| **HOW_TO_RUN.md** | How to execute the compiler | Everyone (start here!) |
| **BEGINNER_GUIDE.md** | Learning basics from scratch | Beginners |
| **USAGE_GUIDE.md** | Complete detailed guide | Learners & students |
| **QUICKSTART.md** | Quick reference & commands | Quick lookup |
| **README.md** | Project overview | Project context |
| **DOCUMENTATION_INDEX.md** | This file! | Navigation |

---

## 🚀 Quick Start Path

### For Absolute Beginners
1. Read: **HOW_TO_RUN.md** (2 min)
2. Run: `python3 main.py input.mc` (1 min)
3. Read: **BEGINNER_GUIDE.md** (10 min)
4. Try: Create your own `.mc` file

### For Experienced Developers
1. Skim: **README.md** (5 min)
2. Run: `python3 main.py input.mc` (1 min)
3. Review: **USAGE_GUIDE.md** (5 min)
4. Explore: Code files (`lexer.py`, `parser.py`, etc)

### For Educators/Presenters
1. Review: **README.md** + **USAGE_GUIDE.md** (15 min)
2. Prepare: Example files to demonstrate
3. Use: **BEGINNER_GUIDE.md** for teaching
4. Demo: Run `python3 interactive.py` live!

---

## 🎓 Learning Paths

### Path 1: "Show Me Quick"
```bash
# 2 minutes
pip3 install ply
python3 main.py input.mc
python3 main.py error_test2.mc
```
Then read: [HOW_TO_RUN.md](HOW_TO_RUN.md)

### Path 2: "Teach Me Concepts"
```bash
# 30 minutes
# 1. Read BEGINNER_GUIDE.md
# 2. Try interactive mode
# 3. Create your own programs
```
Read: [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)

### Path 3: "Deep Dive Learning"
```bash
# 1-2 hours
# 1. Read USAGE_GUIDE.md
# 2. Do all examples
# 3. Explore source code
# 4. Try interactive mode
# 5. Add new features
```
Read: [USAGE_GUIDE.md](USAGE_GUIDE.md)

### Path 4: "I Want to Teach This"
```bash
# Preparation: 1 hour
# 1. Review README.md
# 2. Run all examples
# 3. Read BEGINNER_GUIDE.md
# 4. Prepare demo code
```
Teaching: Use [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) as class material

---

## 💡 Common Questions

### "How do I install it?"
See: **HOW_TO_RUN.md** - Installation section

### "How do I use interactive mode?"
See: **BEGINNER_GUIDE.md** or **USAGE_GUIDE.md** - Interactive Mode section

### "What's a syntax tree?"
See: **BEGINNER_GUIDE.md** - "Understanding the Syntax Tree" section

### "How do I create my own program?"
See: **HOW_TO_RUN.md** or **USAGE_GUIDE.md** - "Examples" section

### "What errors can it detect?"
See: **BEGINNER_GUIDE.md** or **USAGE_GUIDE.md** - "Error Detection" section

### "What language features are supported?"
See: **USAGE_GUIDE.md** - "Supported Syntax" section

### "How do I fix compilation errors?"
See: **BEGINNER_GUIDE.md** - "Common Errors & How to Fix Them"

### "Can I extend this compiler?"
See: **README.md** - "Next Steps" and "Extending the Compiler"

---

## 🏗️ Project Files Structure

### Documentation Files
```
HOW_TO_RUN.md           ← START HERE (how to run)
BEGINNER_GUIDE.md       ← For learning basics
USAGE_GUIDE.md          ← Complete reference
QUICKSTART.md           ← Quick commands
README.md               ← Project overview
DOCUMENTATION_INDEX.md  ← This file!
```

### Compiler Files (Python)
```
main.py         - File-based compiler entry point
interactive.py  - Interactive terminal REPL
lexer.py        - Tokenizer (lexical analysis)
parser.py       - Syntax parser & AST builder
symbol_table.py - Variable tracking (semantic analysis)
```

### Example Code Files (.mc)
```
input.mc        - Valid example (learning)
error_input.mc  - Example with errors (learning)
error_test2.mc  - More complex errors (learning)
```

### Other Files
```
setup.sh        - Setup verification script
.gitignore      - Git ignore rules
```

---

## 📊 What Each Component Does

### Lexer (`lexer.py`)
- Breaks code into tokens
- Identifies keywords, operators, numbers, identifiers
- Detects invalid characters
- Reports character-level errors

**Learn more:** USAGE_GUIDE.md - "Code Structure" section

### Parser (`parser.py`)
- Checks if tokens follow grammar rules
- Builds Abstract Syntax Tree (AST)
- Reports syntax errors
- Validates statement structure

**Learn more:** BEGINNER_GUIDE.md - "Understanding the Syntax Tree"

### Symbol Table (`symbol_table.py`)
- Stores variable declarations
- Tracks variable types
- Checks for duplicate declarations
- Checks for undeclared variable usage

**Learn more:** USAGE_GUIDE.md - "Symbol Table" section

### Main (`main.py`)
- File-based compilation interface
- Displays formatted output
- Shows source code with line numbers
- Displays complete compilation report

**Learn more:** HOW_TO_RUN.md - "Method 1: Compile an Existing File"

### Interactive (`interactive.py`)
- Terminal-based REPL (Read-Eval-Print Loop)
- Accepts line-by-line input
- Shows immediate results
- Supports special commands (END, HELP, CLEAR, QUIT)

**Learn more:** HOW_TO_RUN.md - "Method 3: Interactive Mode"

---

## 🎯 Next Steps After Learning

### Beginner Level
- ✅ Understand basic syntax
- ✅ Run example programs
- ✅ Create simple programs
- ✅ Identify common errors

### Intermediate Level
- ✅ Understand compilation process
- ✅ Read and understand source code
- ✅ Create more complex programs
- ✅ Use interactive mode effectively

### Advanced Level
- ✅ Extend compiler features
- ✅ Add new operators
- ✅ Add control flow (if/while)
- ✅ Add function support
- ✅ Understand language design

### Expert Level
- ✅ Optimize parser
- ✅ Add type checking
- ✅ Generate code/bytecode
- ✅ Build real compiler

---

## 🔗 Quick Links

| Need | Link |
|------|------|
| Install & Run | [HOW_TO_RUN.md](HOW_TO_RUN.md) |
| Learn Basics | [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) |
| Full Guide | [USAGE_GUIDE.md](USAGE_GUIDE.md) |
| Quick Ref | [QUICKSTART.md](QUICKSTART.md) |
| Overview | [README.md](README.md) |

---

## ⚡ TL;DR (Too Long; Didn't Read)

1. **Install:** `pip3 install ply`
2. **Run:** `python3 main.py input.mc`
3. **Learn:** Read [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)
4. **Try:** `python3 interactive.py`
5. **Explore:** Read source code files

---

## 📱 Mobile/Quick Reference

```bash
# Install
pip3 install ply

# Try it
python3 main.py input.mc

# Interactive
python3 interactive.py

# Create file
cat > test.mc << 'EOF'
int x;
x = 42;
EOF

# Compile
python3 main.py test.mc
```

---

## 🎓 For Classroom Use

### 30-Minute Lesson
1. **Intro** (5 min) - Read README.md
2. **Demo** (10 min) - Show examples, run interactive
3. **Activity** (10 min) - Students create programs
4. **Discussion** (5 min) - Discuss errors and AST

### 1-Hour Workshop
1. **Intro** (10 min) - Installation + overview
2. **Guided Tour** (15 min) - Run examples, read guides
3. **Hands-On** (30 min) - Interactive mode + file editing
4. **Discussion** (5 min) - Questions and extensions

### Full Course Module
1. **Week 1** - Learn basics, create simple programs
2. **Week 2** - Understand compilation stages
3. **Week 3** - Read and modify source code
4. **Week 4** - Extend compiler with new features

---

## 📞 Getting Help

**If you're stuck:**

1. **Check the guides:**
   - [HOW_TO_RUN.md](HOW_TO_RUN.md) - How to run
   - [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) - Learning
   - [USAGE_GUIDE.md](USAGE_GUIDE.md) - Details

2. **Try examples:**
   - `python3 main.py input.mc`
   - `python3 main.py error_test2.mc`
   - `python3 interactive.py`

3. **Read error messages:** They usually tell you what's wrong!

4. **Explore source code:** Comments explain everything

---

## ✨ You're All Set!

Pick a guide above and start learning! 🚀

**Recommended first step:** [HOW_TO_RUN.md](HOW_TO_RUN.md)

Happy learning! 🎓
