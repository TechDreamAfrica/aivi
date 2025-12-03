"""
Accessible Study Planner module
"""
def add_event(event):
    # Store events in a local file for offline access
    with open("study_events.txt", "a", encoding="utf-8") as f:
        f.write(f"EVENT: {event}\n")
    print(f"[Planner] Adding event: {event}")

def set_reminder(reminder):
    # Store reminders in a local file for offline access
    with open("study_reminders.txt", "a", encoding="utf-8") as f:
        f.write(f"REMINDER: {reminder}\n")
    print(f"[Planner] Setting reminder: {reminder}")
