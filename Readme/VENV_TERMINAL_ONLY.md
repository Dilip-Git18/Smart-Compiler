# Open Terminal In venv Only (No Install)

This file is only for opening and using terminal in `.venv`.
No package installation commands are included.

## 1) Open venv in current terminal (macOS zsh)

From project folder:

```bash
cd /Users/dilipkumar/Code/Practice/Test/Mini-Compiler
source .venv/bin/activate
```

If activated, terminal prompt usually shows `(.venv)`.

## 2) Verify you are using venv Python

```bash
which python
python --version
```

`which python` should point to `.venv/bin/python`.

## 3) Run project while venv is active

```bash
python main.py input.mc
python interactive.py
```

## 4) Exit venv

```bash
deactivate
```

## 5) VS Code: open new terminal already in venv

In VS Code:

1. `Cmd+Shift+P`
2. Run: `Python: Select Interpreter`
3. Select: `.venv/bin/python`
4. Close old terminals
5. Open a new terminal

New terminal should auto-activate `.venv`.

## 6) One-command start (optional)

If you do not want to activate first, run directly with venv python:

```bash
./.venv/bin/python main.py input.mc
```

This runs in venv without changing shell state.


============================================================
dilipkumar@Dilips-MacBook-Air Mini-Compiler %  source .venv/bin/activate && pyth
on main.py cstyle.mc 2>&1 | tail -24