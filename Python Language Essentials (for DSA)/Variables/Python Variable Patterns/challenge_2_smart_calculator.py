"""
SOLUTION: Challenge 2 - Smart Calculator
Difficulty: Medium
Patterns Used: Dictionary Dispatch, Accumulators, State Variables, Flags
"""

class SmartCalculator:
    def __init__(self):
        # Dictionary dispatch for operations
        self.operations = {
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'multiply': lambda a, b: a * b,
            'divide': lambda a, b: a / b if b != 0 else "Error: Div by 0",
            'power': lambda a, b: a ** b,
            'modulo': lambda a, b: a % b if b != 0 else "Error: Mod by 0"
        }
        
        # State variables
        self.history = []           # Accumulator for history
        self.memory = None          # Memory storage
        self.last_result = None     # For undo
        self.can_undo = False       # Undo flag
    
    def perform(self, operation, a, b):
        """Execute calculation"""
        if operation not in self.operations:
            print(f"❌ Unknown operation: {operation}")
            return None
        
        # Calculate
        result = self.operations[operation](a, b)
        
        # Store in history (accumulator)
        self.history.append({
            'operation': operation,
            'operands': (a, b),
            'result': result
        })
        
        # Update state
        self.last_result = result
        self.can_undo = True
        
        # Display
        symbol = {
            'add': '+', 'subtract': '-', 'multiply': '×',
            'divide': '÷', 'power': '^', 'modulo': '%'
        }.get(operation, operation)
        
        print(f"{a} {symbol} {b} = {result}")
        return result
    
    def show_history(self):
        """Display operation history"""
        print(f"\n📜 CALCULATION HISTORY:")
        print(f"{'='*50}")
        
        if not self.history:
            print("  No operations yet")
        else:
            for i, record in enumerate(self.history, 1):
                op = record['operation']
                a, b = record['operands']
                result = record['result']
                print(f"  {i}. {a} {op} {b} = {result}")
        
        print(f"{'='*50}")
    
    def store_memory(self, value):
        """Store value in memory"""
        self.memory = value
        print(f"💾 Stored {value} in memory")
    
    def recall_memory(self):
        """Recall from memory"""
        if self.memory is None:
            print("📭 Memory is empty")
            return None
        
        print(f"🔍 Recalled from memory: {self.memory}")
        return self.memory
    
    def clear_memory(self):
        """Clear memory"""
        self.memory = None
        print("🗑️ Memory cleared")
    
    def undo(self):
        """Undo last operation"""
        if not self.can_undo or not self.history:
            print("❌ Nothing to undo")
            return
        
        removed = self.history.pop()
        self.can_undo = False
        
        a, b = removed['operands']
        print(f"↩️ Undone: {a} {removed['operation']} {b}")
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.can_undo = False
        print("🗑️ History cleared")


# ============================================================================
# DEMO / TESTING
# ============================================================================

if __name__ == "__main__":
    print("🎯 CHALLENGE 2: SMART CALCULATOR SOLUTION\n")
    
    calc = SmartCalculator()
    
    # Perform calculations
    print("--- Performing Calculations ---")
    calc.perform('add', 15, 7)
    calc.perform('multiply', 6, 8)
    calc.perform('power', 2, 10)
    calc.perform('divide', 144, 12)
    calc.perform('subtract', 100, 37)
    
    # Show history
    calc.show_history()
    
    # Memory operations
    print("\n--- Memory Operations ---")
    calc.store_memory(42)
    calc.perform('add', calc.recall_memory(), 10)
    
    # Undo
    print("\n--- Undo Operation ---")
    calc.undo()
    
    # Show updated history
    calc.show_history()