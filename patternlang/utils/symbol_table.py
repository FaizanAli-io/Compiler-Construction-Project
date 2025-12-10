"""
Symbol table implementation for PatternLang compiler.
Tracks variable declarations, types, and scopes.
"""


class SymbolTable:
    """
    Manages variable symbols during semantic analysis.
    Supports nested scopes (though PatternLang uses simple scoping).
    """

    def __init__(self):
        self.scopes = [{}]  # Stack of scopes, each scope is a dict
        self.current_scope = 0

    def enter_scope(self):
        """Enter a new scope (e.g., inside a repeat block)."""
        self.scopes.append({})
        self.current_scope += 1

    def exit_scope(self):
        """Exit the current scope."""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1

    def declare(self, name, var_type="float", value=None):
        """
        Declare a new variable in the current scope.
        Returns True if successful, False if already declared.
        """
        if name in self.scopes[self.current_scope]:
            return False

        self.scopes[self.current_scope][name] = {
            "type": var_type,
            "value": value,
            "scope": self.current_scope,
        }
        return True

    def lookup(self, name):
        """
        Look up a variable in the current scope and parent scopes.
        Returns the symbol info or None if not found.
        """
        # Search from current scope upwards
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None

    def update(self, name, value):
        """Update the value of an existing variable."""
        # Search from current scope upwards
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                self.scopes[i][name]["value"] = value
                return True
        return False

    def __repr__(self):
        """String representation for debugging."""
        return f"SymbolTable(scopes={self.scopes})"
