"""
ClearCom - Mini C-like Smart Error Detecting Compiler
Main entry point with improved display and AST visualization
"""

import sys
import os
from lexer import build_lexer
from parser import parse, get_errors, get_symbol_table

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
        
        # Show syntax tree if compilation successful
        if ast and not all_errors:
            print("🌳 Syntax Tree (AST):")
            print("-" * 60)
            ast.print_tree()
            print("-" * 60)
            print()
        
        # Print symbol table
        print()
        get_symbol_table().print_table()
        
        # Print results
        print()
        if all_errors:
            print("❌ COMPILATION FAILED")
            print("=" * 60)
            print(f"Total Errors: {len(all_errors)}\n")
            for i, err in enumerate(all_errors, 1):
                print(f"  {i}. ✗ {err}")
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
    print("     python3 main.py <filename.mc>")
    print("     Example: python3 main.py input.mc\n")
    print("  2. INTERACTIVE MODE:")
    print("     python3 interactive.py")
    print("     Write code line by line in the terminal\n")
    print("  3. CREATE YOUR OWN CODE:")
    print("     Create a file with .mc extension")
    print("     Then compile with: python3 main.py myfile.mc\n")
    print("=" * 60 + "\n")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        print_usage()
        print("💡 Tip: Try running: python3 main.py input.mc")
        print("   Or try interactive mode: python3 interactive.py\n")
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

