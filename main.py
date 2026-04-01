"""
ClearCom - Mini C-like Smart Error Detecting Compiler
Main entry point with improved display and AST visualization
"""

import sys
from lexer import build_lexer
from parser import parse, get_errors, get_symbol_table
from executor import execute_program

def compile_file(filename):
    """
    Compile a .mc file with detailed output
    Args:
        filename: path to the .mc file
    """
    try:
        # Read the source file
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"\n{'=' * 60}")
        print(f"           🔧 ClearCom Compiler 🔧")
        print(f"{'=' * 60}\n")
        
        # Print the source code
        print("📄 Source Code:")
        print("-" * 60)
        for i, line in enumerate(source_code.split('\n'), 1):
            print(f"  {i} │ {line}")
        print("-" * 60 + "\n")
        
        # Build lexer
        lexer = build_lexer()
        
        # Parse the code
        print("🔄 Compiling...\n")
        ast = parse(source_code, lexer)
        
        # Check for lexer errors
        lexer_errors = lexer.errors
        
        # Get parser and semantic errors
        errors = get_errors()
        
        # Combine all errors
        all_errors = lexer_errors + errors
        
        # Show AST whenever parser can build one (even partial).
        if ast:
            print("🌳 Syntax Tree (AST):")
            print("-" * 60)
            ast.print_tree()
            print("-" * 60)
            print()
            if all_errors:
                print("ℹ️  Showing partial AST. Fix errors for complete tree.\n")
        elif all_errors:
            print("ℹ️  Syntax Tree not generated due to syntax/lexical errors.\n")
        
        # Print symbol table
        print()
        get_symbol_table().print_table()

        runtime_errors = []
        if ast:
            runtime = execute_program(ast, get_symbol_table())
            runtime_errors = runtime.runtime_errors
            if runtime.output_lines:
                print("\n🧾 Program Output:")
                print("-" * 60)
                for line in runtime.output_lines:
                    print(f"  {line}")
                print("-" * 60)
        
        # Print results
        print()
        total_errors = all_errors + runtime_errors

        if total_errors:
            print("❌ COMPILATION FAILED")
            print("=" * 60)
            print(f"Total Errors: {len(total_errors)}\n")
            for i, err in enumerate(total_errors, 1):
                print(f"  {i}. ✗ {err}")
            print("\nTip: Supported forms include declarations, assignments, expressions,")
            print("and simple C-style 'int main(){...}' with printf/print statements.")
            print("=" * 60)
            return False
        else:
            print("✅ COMPILATION SUCCESSFUL")
            print("=" * 60)
            print("No errors found! Code is valid.")
            print("=" * 60)
            return True
    
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        print("   Make sure the file exists in the current directory.")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def print_usage():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("  ClearCom - Mini C-like Smart Error Detecting Compiler")
    print("=" * 60)
    print("\n📖 Usage:\n")
    print("  1. COMPILE A FILE:")
    print("     ./.venv/bin/python main.py <filename.mc>")
    print("     Example: ./.venv/bin/python main.py input.mc\n")
    print("  2. INTERACTIVE MODE:")
    print("     ./.venv/bin/python interactive.py")
    print("     Write code line by line in the terminal\n")
    print("  3. CREATE YOUR OWN CODE:")
    print("     Create a file with .mc extension")
    print("     Then compile with: ./.venv/bin/python main.py myfile.mc\n")
    print("=" * 60 + "\n")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        print_usage()
        print("💡 Tip: Try running: ./.venv/bin/python main.py input.mc")
        print("   Or try interactive mode: ./.venv/bin/python interactive.py\n")
        sys.exit(0)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        success = compile_file(filename)
        sys.exit(0 if success else 1)
    else:
        print("❌ Invalid arguments!")
        print_usage()
        sys.exit(1)

if __name__ == '__main__':
    main()

