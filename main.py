"""
ClearCom - Mini C-like Smart Error Detecting Compiler
Main entry point with improved display
"""

import sys
from compiler_service import compile_source


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

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
        
        print("🔄 Compiling...\n")
        result = compile_source(source_code, trace=False)

        print(f"{CYAN}Symbol Table:{RESET}")
        print("-" * 60)
        if result["symbols"]:
            for name, typ in result["symbols"].items():
                value = result.get("runtimeValues", {}).get(name)
                print(f"  {name:15} : {typ:5} value={value}")
        else:
            print("  Empty")
        print("-" * 60)

        if result["output"]:
            print(f"\n{CYAN}🧾 Program Output:{RESET}")
            print("-" * 60)
            for line in result["output"]:
                print(f"  {line}")
            print("-" * 60)

        if result.get("warnings"):
            print(f"\n{YELLOW}⚠ Warnings ({len(result['warnings'])}):{RESET}")
            for i, warn in enumerate(result["warnings"], 1):
                print(f"  {i}. {warn}")

        total_errors = result["errors"]

        if total_errors:
            print(f"{RED}❌ COMPILATION FAILED{RESET}")
            print("=" * 60)
            print(f"Total Errors: {len(total_errors)}\n")
            for i, err in enumerate(total_errors, 1):
                print(f"  {RED}{i}. ✗ {err}{RESET}")
            print("\nTip: Supported forms include declarations, assignments, expressions,")
            print("and simple C-style 'int main(){...}' with printf/print statements.")
            print("=" * 60)
            return False
        else:
            print(f"{GREEN}✅ COMPILATION SUCCESSFUL{RESET}")
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

