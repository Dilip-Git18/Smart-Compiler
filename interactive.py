"""
Interactive Mode for ClearCom Compiler
Allows users to write and compile code interactively in the terminal
"""

from lexer import build_lexer
from parser import parse, get_errors, get_symbol_table

def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 60)
    print("         🔧 ClearCom Interactive Compiler 🔧")
    print("=" * 60)
    print("\n📝 Commands:")
    print("  • Type your code line by line")
    print("  • Type 'END' to finish (on new line)")
    print("  • Type 'HELP' for syntax help")
    print("  • Type 'CLEAR' to start over")
    print("  • Type 'QUIT' to exit")
    print("\n" + "-" * 60 + "\n")

def print_help():
    """Print syntax help"""
    print("\n📚 ClearCom Syntax Help:")
    print("-" * 60)
    print("Variables (declaration):")
    print("  int x;")
    print("  float pi;")
    print("\nAssignment:")
    print("  x = 10;")
    print("  pi = 3.14;")
    print("\nExpressions:")
    print("  x = 5 + 3;")
    print("  y = x * 2;")
    print("  result = (a + b) / 2;")
    print("\nOperators: + - * / %")
    print("-" * 60 + "\n")

def get_user_input():
    """Get multi-line input from user"""
    print("Enter your code (type 'END' on a new line to compile):")
    print("Type 'HELP' for help, 'CLEAR' to reset, 'QUIT' to exit\n")
    
    lines = []
    line_num = 1
    
    while True:
        try:
            prompt = f"  {line_num} > "
            user_input = input(prompt).strip()
            
            # Handle special commands
            if user_input.upper() == 'END':
                break
            elif user_input.upper() == 'HELP':
                print_help()
                continue
            elif user_input.upper() == 'CLEAR':
                print("✓ Code cleared. Start over.\n")
                return None
            elif user_input.upper() == 'QUIT':
                print("👋 Goodbye!\n")
                return False
            
            if user_input:  # Only add non-empty lines
                lines.append(user_input)
                line_num += 1
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            return False
        except EOFError:
            break
    
    if not lines:
        print("⚠️  No code entered.\n")
        return None
    
    return '\n'.join(lines)

def compile_and_show(code):
    """Compile code and display results"""
    print("\n" + "-" * 60)
    print("📊 COMPILATION REPORT")
    print("-" * 60)
    
    # Show source code
    print("\n📄 Source Code:")
    print("-" * 40)
    for i, line in enumerate(code.split('\n'), 1):
        print(f"  {i} │ {line}")
    print("-" * 40)
    
    # Build lexer
    lexer = build_lexer()
    
    # Parse code
    print("\n🔄 Compiling...\n")
    ast = parse(code, lexer)
    
    # Check for lexer errors
    lexer_errors = lexer.errors
    
    # Get parser and semantic errors
    errors = get_errors()
    
    # Combine all errors
    all_errors = lexer_errors + errors
    
    # Show syntax tree
    if ast and not all_errors:
        print("🌳 Syntax Tree:")
        print("-" * 40)
        ast.print_tree()
        print("-" * 40)
        print()
    
    # Print symbol table
    print()
    get_symbol_table().print_table()
    
    # Print results
    print()
    if all_errors:
        print("❌ COMPILATION FAILED")
        print("-" * 60)
        print(f"Errors: {len(all_errors)}")
        for i, err in enumerate(all_errors, 1):
            print(f"  {i}. ✗ {err}")
        print("-" * 60)
        return False
    else:
        print("✅ COMPILATION SUCCESSFUL")
        print("-" * 60)
        print("No errors found! Code is valid.")
        print("-" * 60)
        return True

def interactive_mode():
    """Run interactive compiler session"""
    print_banner()
    
    while True:
        result = get_user_input()
        
        if result is False:
            break
        elif result is None:
            continue
        
        compile_and_show(result)
        
        # Ask if user wants to compile more
        try:
            print("\n" + "=" * 60)
            response = input("Compile more code? (yes/no): ").strip().upper()
            if response not in ['Y', 'YES']:
                print("👋 Thank you for using ClearCom!\n")
                break
            print()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!\n")
            break

if __name__ == '__main__':
    interactive_mode()
