"""
AIVI Splash Screen Launcher
Standalone splash screen that can launch before the main application
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os

# Add the parent directory to sys.path so we can import from ai_assistant
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import ai_assistant.tts as tts
except ImportError:
    tts = None

def safe_tts_speak(text):
    """Safely speak text with TTS if available"""
    if tts:
        try:
            # Use TTS directly without threading to avoid GUI conflicts
            tts.speak_text(text)
        except Exception as e:
            print(f"TTS Error: {e}")

class StandaloneSplashScreen:
    def __init__(self, callback=None):
        self.callback = callback
        
        # Initialize counters and control flags first
        self.loading_step = 0
        self.animation_counter = 0
        self.current_progress = 0  # Track smooth progress animation
        self.is_running = True  # Flag to control animations
        self.animation_job = None  # Store animation job ID for cancellation
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("AIVI Loading...")
        self.root.geometry("750x600")
        self.root.configure(bg='#000000')
        self.root.resizable(False, False)
        
        # Remove window decorations for a clean splash look
        self.root.overrideredirect(True)
        
        # Center on screen
        self.center_window()
        
        # Create splash content
        self.create_splash_content()
        
        # Don't start loading here anymore - it's now started in create_splash_content()
    
    def is_alive(self):
        """Check if the splash screen is still active"""
        try:
            return self.is_running and hasattr(self, 'root') and self.root.winfo_exists()
        except (tk.TclError, AttributeError):
            return False
    
    def get_window(self):
        """Get the root window (for external access)"""
        return self.root if self.is_alive() else None
    
    def center_window(self):
        """Center the splash screen on the display"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_splash_content(self):
        """Create the splash screen content"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#000000', padx=40, pady=40)
        main_frame.pack(fill='both', expand=True)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg='#000000')
        header_frame.pack(pady=(20, 30))
        
        # Logo section with multiple accessibility symbols
        logo_frame = tk.Frame(header_frame, bg='#000000')
        logo_frame.pack()
        
        # Accessibility symbols
        symbols = ["♿", "👁️", "🎓", "🖥️"]
        for i, symbol in enumerate(symbols):
            symbol_label = tk.Label(logo_frame,
                                   text=symbol,
                                   font=('Segoe UI', 24, 'bold'),
                                   fg='#00bfff',
                                   bg='#000000')
            symbol_label.grid(row=0, column=i, padx=5)
        
        # Main title
        title_label = tk.Label(header_frame,
                              text="AIVI",
                              font=('Segoe UI', 56, 'bold'),
                              fg='#00bfff',
                              bg='#000000')
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="AI Assistant for Education & Accessibility",
                                 font=('Segoe UI', 18, 'bold'),
                                 fg='#ffffff',
                                 bg='#000000')
        subtitle_label.pack(pady=(0, 10))
        
        # Feature highlights
        features_text = "Voice Control • Desktop Apps • Academic Support • Accessibility Tools"
        features_label = tk.Label(header_frame,
                                 text=features_text,
                                 font=('Segoe UI', 12, 'bold'),
                                 fg='#f0f0f0',
                                 bg='#000000')
        features_label.pack(pady=(10, 0))
        
        # Loading section
        loading_frame = tk.Frame(main_frame, bg='#000000')
        loading_frame.pack(pady=(40, 20))
        
        # Loading animation (spinning dots)
        self.loading_animation = tk.Label(loading_frame,
                                         text="●○○○",
                                         font=('Segoe UI', 20, 'bold'),
                                         fg='#00ff00',
                                         bg='#000000')
        self.loading_animation.pack(pady=(0, 10))
        
        # Loading message with icon
        loading_msg_frame = tk.Frame(loading_frame, bg='#000000')
        loading_msg_frame.pack()
        
        self.loading_icon = tk.Label(loading_msg_frame,
                                    text="⚡",
                                    font=('Segoe UI', 16),
                                    fg='#00ff00',
                                    bg='#000000')
        self.loading_icon.pack(side='left', padx=(0, 8))
        
        self.loading_label = tk.Label(loading_msg_frame,
                                     text="Initializing AIVI System...",
                                     font=('Segoe UI', 14, 'bold'),
                                     fg='#00ff00',
                                     bg='#000000')
        self.loading_label.pack(side='left')
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg='#000000')
        progress_frame.pack(pady=(20, 20))
        
        # Progress bar (enhanced configuration)
        self.progress_var = tk.DoubleVar()
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       foreground='#00ff00',
                       background='#00ff00',
                       darkcolor='#003300',
                       lightcolor='#00ff00',
                       bordercolor='#00bfff',
                       borderwidth=2,
                       troughcolor='#1a1a1a')
        
        # Create progress bar without height parameter
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           variable=self.progress_var,
                                           maximum=100,
                                           length=600,
                                           style="Custom.Horizontal.TProgressbar",
                                           mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Percentage and status
        status_frame = tk.Frame(progress_frame, bg='#000000')
        status_frame.pack(pady=(10, 0))
        
        self.percentage_label = tk.Label(status_frame,
                                        text="0%",
                                        font=('Segoe UI', 12, 'bold'),
                                        fg='#00ff00',
                                        bg='#000000')
        self.percentage_label.pack()
        
        self.status_label = tk.Label(status_frame,
                                    text="Loading system components...",
                                    font=('Segoe UI', 10),
                                    fg='#cccccc',
                                    bg='#000000')
        self.status_label.pack(pady=(5, 0))
        
        # Footer section
        footer_frame = tk.Frame(main_frame, bg='#000000')
        footer_frame.pack(side='bottom', pady=(30, 20))
        
        # Instructions
        instructions_label = tk.Label(footer_frame,
                                     text="Press SPACEBAR to activate voice control once loaded",
                                     font=('Segoe UI', 11, 'bold'),
                                     fg='#ffff00',
                                     bg='#000000')
        instructions_label.pack(pady=(0, 10))
        
        # Version info
        version_label = tk.Label(footer_frame,
                                text="Version 2.0 - Enhanced Edition with Desktop Control & Voice AI",
                                font=('Segoe UI', 10, 'bold'),
                                fg='#f0f0f0',
                                bg='#000000')
        version_label.pack()
        
        # Copyright
        copyright_label = tk.Label(footer_frame,
                                  text="Designed for Visual Accessibility • Voice-First Interface • Educational Support",
                                  font=('Segoe UI', 9),
                                  fg='#999999',
                                  bg='#000000')
        copyright_label.pack(pady=(5, 0))
        
        # Start animation after all components are created
        self.animate_loading()
        
        # Start loading sequence after a brief delay to ensure UI is rendered
        self.root.after(500, self.start_loading)
    
    def animate_loading(self):
        """Animate the loading dots"""
        # Check if the window is still running and exists
        if not self.is_alive():
            return
            
        try:
            animations = ["●○○○", "○●○○", "○○●○", "○○○●", "○○●○", "○●○○"]
            
            # Use separate animation counter to avoid conflicts with loading_step
            current_animation = animations[self.animation_counter % len(animations)]
            if hasattr(self, 'loading_animation'):
                self.loading_animation.config(text=current_animation)
            
            self.animation_counter += 1
            
            # Continue animation only if still running
            if self.is_alive():
                self.animation_job = self.root.after(200, self.animate_loading)
        except (tk.TclError, AttributeError):
            # Window has been destroyed, stop animation
            self.is_running = False
            self.animation_job = None
    
    def start_loading(self):
        """Start the loading sequence with smooth progress animation"""
        loading_steps = [
            {
                "message": "Initializing AIVI Core System...",
                "status": "Loading AI assistant framework and core libraries",
                "icon": "🤖",
                "delay": 800,
                "progress_increment": 8
            },
            {
                "message": "Scanning Desktop Applications...",
                "status": "Detecting Microsoft Office, browsers, and system tools",
                "icon": "🖥️",
                "delay": 700,
                "progress_increment": 8
            },
            {
                "message": "Configuring Voice Recognition...",
                "status": "Setting up speech recognition and natural language processing",
                "icon": "🎙️",
                "delay": 900,
                "progress_increment": 10
            },
            {
                "message": "Loading Text-to-Speech Engine...",
                "status": "Initializing voice synthesis and accessibility features",
                "icon": "🔊",
                "delay": 600,
                "progress_increment": 8
            },
            {
                "message": "Preparing Academic Knowledge Base...",
                "status": "Loading offline educational content and Q&A system",
                "icon": "📚",
                "delay": 800,
                "progress_increment": 10
            },
            {
                "message": "Setting Up Accessibility Tools...",
                "status": "Configuring screen reader, OCR, and Braille support",
                "icon": "♿",
                "delay": 700,
                "progress_increment": 8
            },
            {
                "message": "Initializing Conversation AI...",
                "status": "Loading natural conversation and emotional intelligence",
                "icon": "💬",
                "delay": 900,
                "progress_increment": 10
            },
            {
                "message": "Configuring Study Tools...",
                "status": "Setting up math solver, note-taking, and study planner",
                "icon": "📝",
                "delay": 600,
                "progress_increment": 8
            },
            {
                "message": "Preparing Desktop Integration...",
                "status": "Setting up application launching and system control",
                "icon": "⚙️",
                "delay": 700,
                "progress_increment": 8
            },
            {
                "message": "Loading User Interface...",
                "status": "Preparing high-contrast GUI and keyboard navigation",
                "icon": "🎨",
                "delay": 800,
                "progress_increment": 10
            },
            {
                "message": "Finalizing System Setup...",
                "status": "Completing initialization and running system checks",
                "icon": "🔧",
                "delay": 600,
                "progress_increment": 8
            },
            {
                "message": "AIVI Ready to Assist!",
                "status": "All systems loaded successfully - Welcome to your AI Assistant!",
                "icon": "✅",
                "delay": 1200,
                "progress_increment": 4
            }
        ]

        if not self.is_alive():
            return

        if self.loading_step < len(loading_steps):
            current_step = loading_steps[self.loading_step]

            try:
                # Update loading message and icon
                if hasattr(self, 'loading_icon'):
                    self.loading_icon.config(text=current_step["icon"])
                if hasattr(self, 'loading_label'):
                    self.loading_label.config(text=current_step["message"])
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=current_step["status"])

                # Start smooth progress animation for this step
                self.animate_progress_to_step(current_step["progress_increment"], current_step["delay"])

                # Voice feedback
                if self.loading_step == 0:
                    safe_tts_speak("Welcome to AIVI. Loading your AI Assistant for Education and Accessibility.")
                elif self.loading_step == len(loading_steps) - 1:
                    safe_tts_speak("AIVI is ready! Your voice-controlled assistant is now available.")

            except (tk.TclError, AttributeError) as e:
                # Window components have been destroyed
                print(f"Error updating UI components: {e}")
                self.is_running = False
                return

            self.loading_step += 1

            # Continue loading
            if self.loading_step < len(loading_steps) and self.is_alive():
                self.root.after(current_step["delay"], self.start_loading)
            else:
                # Finished loading
                if self.is_alive():
                    self.root.after(1000, self.finish_loading)

    def animate_progress_to_step(self, increment, total_delay):
        """Smoothly animate progress bar to the next step"""
        if not hasattr(self, 'current_progress'):
            self.current_progress = 0

        target_progress = self.current_progress + increment
        steps = 20  # Number of animation frames
        step_size = increment / steps
        step_delay = total_delay // steps

        self.animate_progress_frame(target_progress, step_size, step_delay, 0, steps)

    def animate_progress_frame(self, target_progress, step_size, step_delay, current_frame, total_frames):
        """Animate a single frame of the progress bar"""
        if not self.is_alive() or current_frame >= total_frames:
            return

        try:
            # Update progress
            if not hasattr(self, 'current_progress'):
                self.current_progress = 0

            self.current_progress += step_size

            # Ensure we don't exceed the target
            if self.current_progress > target_progress:
                self.current_progress = target_progress

            # Update progress bar color based on completion
            self.update_progress_color(self.current_progress)

            # Update UI
            if hasattr(self, 'progress_var'):
                self.progress_var.set(self.current_progress)
                self.root.update_idletasks()

            if hasattr(self, 'percentage_label'):
                self.percentage_label.config(text=f"{int(self.current_progress)}%")

            # Continue animation
            if current_frame < total_frames - 1 and self.is_alive():
                self.root.after(step_delay, lambda: self.animate_progress_frame(
                    target_progress, step_size, step_delay, current_frame + 1, total_frames))

        except (tk.TclError, AttributeError) as e:
            print(f"Error in progress animation: {e}")
            self.is_running = False

    def update_progress_color(self, progress):
        """Update progress bar color based on completion percentage"""
        try:
            if not hasattr(self, 'progress_bar'):
                return

            style = ttk.Style()

            # Color transitions based on progress
            if progress < 25:
                # Early stages - cyan to green
                color = '#00bfff'
            elif progress < 50:
                # Mid-early stages - green
                color = '#00ff00'
            elif progress < 75:
                # Mid-late stages - yellow-green
                color = '#7fff00'
            elif progress < 95:
                # Almost complete - yellow
                color = '#ffff00'
            else:
                # Complete - bright green
                color = '#00ff00'

            style.configure("Custom.Horizontal.TProgressbar",
                           foreground=color,
                           background=color,
                           lightcolor=color)

        except Exception as e:
            print(f"Error updating progress color: {e}")
        
    def finish_loading(self):
        """Finish loading and execute callback or close"""
        if not self.is_alive():
            return
            
        # Stop animations immediately
        self.is_running = False
        
        # Cancel any pending animation jobs
        if self.animation_job:
            try:
                self.root.after_cancel(self.animation_job)
                self.animation_job = None
            except Exception as e:
                print(f"Warning: Could not cancel animation job: {e}")
                pass
        
        if self.callback:
            try:
                # Run callback in next mainloop iteration to ensure clean execution
                self.root.after(100, self._run_callback_and_close)
                return
            except Exception as e:
                print(f"Error scheduling callback: {e}")
        
        # If no callback, close immediately
        self._close_splash()
    
    def _run_callback_and_close(self):
        """Run the callback and then close the splash"""
        try:
            if self.callback:
                self.callback()
        except Exception as e:
            print(f"Error in callback: {e}")
        finally:
            self._close_splash()
    
    def _close_splash(self):
        """Safely close the splash screen"""
        self.is_running = False
        
        # Cancel any pending jobs
        if self.animation_job:
            try:
                self.root.after_cancel(self.animation_job)
            except Exception as e:
                print(f"Warning: Could not cancel pending animation job: {e}")
                pass
            self.animation_job = None
        
        try:
            if hasattr(self, 'root') and self.root.winfo_exists():
                self.root.quit()  # Exit mainloop
                self.root.destroy()
        except (tk.TclError, AttributeError):
            # Window already destroyed
            pass
    
    def show(self):
        """Show the splash screen"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error in splash screen: {e}")
        finally:
            # Ensure animations are stopped
            self.is_running = False

def launch_aivi_with_splash():
    """Launch AIVI with the standalone splash screen"""
    def start_main_app():
        """Start the main AIVI application"""
        try:
            # Import and run the main GUI
            import main
            app = main.ModernAIVIGUI(show_splash=False)  # Don't show splash again
            app.run()
        except ImportError:
            print("Error: Could not import main module. Make sure the main application file exists.")
        except AttributeError:
            print("Error: ModernAIVIGUI class not found in main module.")
        except Exception as e:
            print(f"Error launching main application: {e}")
    
    # Show splash screen first
    splash = StandaloneSplashScreen(callback=start_main_app)
    splash.show()

def main():
    """Main entry point"""
    print("Starting AIVI with Enhanced Splash Screen...")
    launch_aivi_with_splash()

if __name__ == "__main__":
    main()