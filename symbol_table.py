"""
Symbol Table for ClearCom - manages variables and their types
Performs semantic checks for duplicate and undeclared variables
"""

class SymbolTable:
    """
    Manages variable declarations and type information
    """
    def __init__(self):
        self.symbols = {}  # {'var_name': 'int'/'float'}
        self.declared_at = {}
        self.read_usage = {}
        self.errors = []
    
    def declare(self, var_name, var_type, line):
        """
        Declare a new variable
        Args:
            var_name: name of the variable
            var_type: type (int or float)
            line: line number where declared
        """
        if var_name in self.symbols:
            error_msg = f"Line {line}: Duplicate variable '{var_name}' (previously declared)"
            self.errors.append(error_msg)
            return False
        
        self.symbols[var_name] = var_type
        self.declared_at[var_name] = line
        self.read_usage[var_name] = 0
        return True
    
    def lookup(self, var_name, line):
        """
        Check if variable is declared
        Args:
            var_name: name of variable to look up
            line: line number for error reporting
        Returns:
            var_type if found, None if not declared
        """
        if var_name not in self.symbols:
            error_msg = f"Line {line}: Undeclared variable '{var_name}'"
            self.errors.append(error_msg)
            return None
        
        return self.symbols[var_name]

    def mark_read(self, var_name):
        """Mark variable as read in an expression/print context."""
        if var_name in self.read_usage:
            self.read_usage[var_name] += 1

    def get_unused_warnings(self):
        """Return warnings for declared but never-read variables."""
        warnings = []
        for var_name, count in self.read_usage.items():
            if count == 0:
                line = self.declared_at.get(var_name, "?")
                warnings.append(
                    f"Line {line}: Variable '{var_name}' is declared but never used"
                )
        return warnings
    
    def get_type(self, var_name):
        """Get the type of a declared variable"""
        return self.symbols.get(var_name)
    
    def print_table(self):
        """Print the symbol table"""
        if self.symbols:
            print("\nSymbol Table:")
            print("-" * 30)
            for var_name, var_type in self.symbols.items():
                print(f"  {var_name:15} : {var_type}")
            print("-" * 30)
        else:
            print("Symbol Table: Empty")
