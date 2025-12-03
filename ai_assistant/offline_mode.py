"""
Offline Mode module
"""
def enable_offline_mode():
    # Set a global flag or config file to indicate offline mode
    import os
    with open("offline_mode.flag", "w") as f:
        f.write("offline")
    print("[Offline] Offline mode enabled.")

def disable_offline_mode():
    # Remove the offline mode flag to disable offline mode
    import os
    try:
        if os.path.exists("offline_mode.flag"):
            os.remove("offline_mode.flag")
        print("[Online] Online mode enabled.")
    except Exception as e:
        print(f"[Error] Could not disable offline mode: {e}")
