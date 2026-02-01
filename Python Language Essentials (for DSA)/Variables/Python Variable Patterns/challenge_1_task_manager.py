"""
SOLUTION: Challenge 1 - Task Manager
Difficulty: Easy
Patterns Used: Lists, Dictionaries, Flags, Counters
"""

class TaskManager:
    def __init__(self):
        self.tasks = []              # List to store tasks
        self.task_priorities = {}    # Dictionary for priorities
        self.completed_flags = {}    # Flags for completion
        self.task_id_counter = 0     # Counter for unique IDs
    
    def add_task(self, description, priority='medium'):
        """Add a new task with priority"""
        self.task_id_counter += 1
        task_id = self.task_id_counter
        
        # Add to list
        self.tasks.append({
            'id': task_id,
            'description': description
        })
        
        # Set priority
        self.task_priorities[task_id] = priority
        
        # Initialize completion flag
        self.completed_flags[task_id] = False
        
        print(f"✅ Task #{task_id} added: {description} [{priority}]")
        return task_id
    
    def mark_complete(self, task_id):
        """Mark a task as complete"""
        if task_id in self.completed_flags:
            self.completed_flags[task_id] = True
            print(f"🎉 Task #{task_id} marked complete!")
        else:
            print(f"❌ Task #{task_id} not found")
    
    def show_summary(self):
        """Display task summary"""
        total = len(self.tasks)
        completed = sum(1 for done in self.completed_flags.values() if done)
        pending = total - completed
        
        print(f"\n📊 TASK SUMMARY")
        print(f"{'='*40}")
        print(f"Total Tasks:      {total}")
        print(f"Completed:        {completed}")
        print(f"Pending:          {pending}")
        print(f"Completion Rate:  {(completed/total*100):.1f}%" if total > 0 else "No tasks")
        print(f"{'='*40}")
    
    def list_high_priority(self):
        """List all high-priority tasks"""
        print(f"\n🔥 HIGH PRIORITY TASKS:")
        print(f"{'-'*40}")
        
        found = False
        for task in self.tasks:
            task_id = task['id']
            if self.task_priorities[task_id] == 'high':
                status = "✓" if self.completed_flags[task_id] else "○"
                print(f"  {status} #{task_id}: {task['description']}")
                found = True
        
        if not found:
            print("  No high-priority tasks")
        print(f"{'-'*40}")


# ============================================================================
# DEMO / TESTING
# ============================================================================

if __name__ == "__main__":
    print("🎯 CHALLENGE 1: TASK MANAGER SOLUTION\n")
    
    # Create task manager
    tm = TaskManager()
    
    # Add tasks
    tm.add_task("Fix critical bug in login", "high")
    tm.add_task("Update documentation", "low")
    tm.add_task("Code review PR #42", "high")
    tm.add_task("Team meeting at 2pm", "medium")
    tm.add_task("Optimize database queries", "high")
    
    # Mark some complete
    print("\n--- Completing Tasks ---")
    tm.mark_complete(1)
    tm.mark_complete(4)
    tm.mark_complete(5)
    
    # Show summary
    tm.show_summary()
    
    # List high priority
    tm.list_high_priority()