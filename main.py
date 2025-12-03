import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
import platform
import ctypes
from datetime import datetime

# Windows COM initialization fix

def request_admin_privileges():
    """Request administrator privileges for the application"""
    if platform.system() == "Windows":
        try:
            # Check if already running as administrator
            if ctypes.windll.shell32.IsUserAnAdmin():
                return True
            else:
                # Re-run the program with admin rights
                script_path = os.path.abspath(sys.argv[0])
                params = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''

                # Use ShellExecute with 'runas' verb to trigger UAC
                result = ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script_path}" {params}', None, 1
                )

                if result > 32:  # Success
                    sys.exit(0)  # Exit current process as admin version will start
                else:
                    return False
        except Exception as e:
            print(f"Failed to request admin privileges: {e}")
            return False
    return True  # Non-Windows systems

from splash_launcher import StandaloneSplashScreen

# Import AI assistant modules (with optional dependencies)
import ai_assistant.tts as tts
import ai_assistant.offline_academic as offline_academic
import ai_assistant.math_reader as math_reader
import ai_assistant.study_planner as study_planner
import ai_assistant.content_search as content_search
import ai_assistant.multi_modal as multi_modal
import ai_assistant.offline_mode as offline_mode
import ai_assistant.desktop_control as desktop_control
import ai_assistant.offline_conversation as offline_conversation

# Enhanced modules for offline-first functionality
try:
    from ai_assistant.offline_manager import OfflineDataManager
except ImportError:
    OfflineDataManager = None

try:
    from ai_assistant.enhanced_voice_manager import EnhancedVoiceManager
except ImportError:
    EnhancedVoiceManager = None

try:
    from ai_assistant.google_search_manager import GoogleSearchManager
except ImportError:
    GoogleSearchManager = None

# Import conversation memory system
try:
    from ai_assistant.conversation_memory import (
        get_memory, add_user_message, add_assistant_message,
        save_current_session, get_conversation_context, get_user_stats
    )
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠ Conversation memory system not available")

# Optional imports that may fail due to missing dependencies
try:
    import ai_assistant.voice_commands as voice_commands
except ImportError:
    voice_commands = None

try:
    import ai_assistant.offline_voice_control as offline_voice
except ImportError:
    offline_voice = None

try:
    import ai_assistant.qa_tutoring as qa_tutoring
except ImportError:
    qa_tutoring = None

try:
    import ai_assistant.braille as braille
except ImportError:
    braille = None

# Import OpenAI for search functionality
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def safe_tts_speak(text, app_instance=None):
    """Safely speak text without threading issues, using saved voice settings"""
    try:
        # Get voice settings if app instance is available
        voice_settings = None
        if app_instance and hasattr(app_instance, 'voice_settings'):
            voice_settings = app_instance.voice_settings

        # Use saved settings or defaults
        if voice_settings:
            voice = voice_settings.get('voice_gender', 'default')
            speed = voice_settings.get('speech_speed', 1.0)
            volume = voice_settings.get('speech_volume', 1.0)
            tts.speak_text(text, voice=voice, speed=speed)
        else:
            # Use default settings
            tts.speak_text(text)
    except Exception as e:
        print(f"TTS Error: {e}")


class ModernAIVIGUI:
    def __init__(self, show_splash=True):
        self.root = tk.Tk()
        self.root.title("AIVI - AI Assistant")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Initialize cleanup tracking
        self.timer_job = None
        self.resize_job = None
        self.is_running = True
        
        try:
            self.root.iconbitmap("aivi.ico")
        except tk.TclError:
            print("Icon file not found, using default icon")
                
        # Hide main window initially if showing splash
        if show_splash:
            self.root.withdraw()
            
        # Set up proper cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # High-contrast color scheme for visual accessibility
        self.colors = {
            'bg': '#000000',           # Pure black background for maximum contrast
            'card_bg': '#1a1a1a',      # Very dark card background
            'accent': '#00bfff',       # Bright cyan blue - high visibility
            'accent_hover': '#0099cc', # Darker cyan for hover
            'secondary': '#4a5568',    # Dark gray for secondary buttons
            'success': '#00ff00',      # Bright green - high contrast
            'warning': '#ffff00',      # Bright yellow - high visibility
            'error': '#ff0000',        # Bright red - maximum visibility
            'text': '#ffffff',         # Pure white text for maximum contrast
            'text_secondary': '#f0f0f0', # Very light gray - still high contrast
            'border': '#666666',       # Medium gray for visible borders
            'input_bg': '#333333',     # Dark gray for input fields
            'button_text': '#000000'   # Black text for bright buttons
        }
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.is_listening = False
        self.is_offline_mode = os.path.exists("offline_mode.flag")
        
        # Enhanced offline-first components
        self.offline_data = None
        self.enhanced_voice_manager = None
        self.google_search_manager = None
        self.search_mode = "offline_first"  # offline_first, google_first, ai_only
        
        # Initialize enhanced components
        self.initialize_enhanced_components()
        
        # Show splash screen if requested
        if show_splash:
            self.show_splash_screen()
        else:
            self.initialize_gui()
    
    def initialize_enhanced_components(self):
        """Initialize enhanced offline-first components"""
        try:
            # Initialize offline data manager
            if OfflineDataManager:
                self.offline_data = OfflineDataManager()
                print("✓ Offline data manager initialized")
            else:
                print("⚠ OfflineDataManager not available")
                
            # Initialize enhanced voice manager
            if EnhancedVoiceManager and self.offline_data:
                self.enhanced_voice_manager = EnhancedVoiceManager(self.offline_data)
                print("✓ Enhanced voice manager initialized")
            else:
                print("⚠ EnhancedVoiceManager not available")
                
            # Initialize Google search manager
            if GoogleSearchManager and self.offline_data:
                self.google_search_manager = GoogleSearchManager(self.offline_data)
                print("✓ Google search manager initialized")
            else:
                print("⚠ GoogleSearchManager not available")
                
        except Exception as e:
            print(f"⚠ Error initializing enhanced components: {e}")
    
    def show_splash_screen(self):
        """Show the splash screen and then initialize GUI"""
        splash = StandaloneSplashScreen()
        
        # Wait for splash to finish, then show main window
        def check_splash():
            try:
                # Fixed: Use splash.is_alive() instead of splash.splash.winfo_exists()
                if splash.is_alive():
                    self.root.after(100, check_splash)
                else:
                    self.initialize_gui()
            except (tk.TclError, AttributeError):
                # Splash closed or destroyed
                self.initialize_gui()
        
        # Start the splash screen in a separate thread or window
        splash.show()
        
        # Start checking for splash completion
        self.root.after(100, check_splash)
    
    def initialize_gui(self):
        """Initialize the main GUI after splash screen"""
        # Show main window
        self.root.deiconify()
        
        # Create GUI
        self.create_gui()
        
        # Bind keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Status
        self.update_status("Ready - Press SPACEBAR for voice, F1 for help, ESC to stop voice", "success")
        
        # Voice welcome message
        welcome_msg = "AIVI is now ready! Press spacebar to activate voice commands, or type your questions in the chat."
        safe_tts_speak(welcome_msg, self)
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg=self.colors['bg'])
        
        # Button styles
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_hover'])])
        
        style.configure('Card.TFrame',
                       background=self.colors['card_bg'],
                       relief='flat',
                       borderwidth=1)
        
        # Notebook style
        style.configure('Modern.TNotebook',
                       background=self.colors['bg'],
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       padding=(20, 10),
                       borderwidth=0)
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['accent_hover'])])
    
    def safe_after(self, delay, callback, *args):
        """
        Safely schedule a callback that checks if the widget still exists
        This prevents 'invalid command name' errors
        """
        def safe_callback():
            try:
                if self.is_running and self.root.winfo_exists():
                    callback(*args)
            except tk.TclError:
                # Widget was destroyed, ignore
                pass
            except Exception as e:
                print(f"Error in callback: {e}")

        try:
            return self.root.after(delay, safe_callback)
        except tk.TclError:
            # Root was destroyed
            pass

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for accessibility"""
        # Bind spacebar to toggle voice mode
        self.root.bind('<KeyPress-space>', self.spacebar_voice_toggle)
        
        # Bind F1 for help
        self.root.bind('<F1>', self.show_help)
        
        # Bind Escape to stop voice mode
        self.root.bind('<Escape>', self.stop_voice_mode)
        
        # Make sure the root window can receive focus for key events
        self.root.focus_set()
    
    def spacebar_voice_toggle(self, event=None):
        """Handle spacebar press to toggle voice mode"""
        # Only trigger if spacebar is pressed and not in an input field
        focused_widget = self.root.focus_get()
        
        # Check if focus is on an input field (Entry or Text widgets)
        if (isinstance(focused_widget, tk.Entry) or 
            isinstance(focused_widget, tk.Text) or
            (hasattr(focused_widget, 'winfo_class') and 
             focused_widget.winfo_class() in ['Entry', 'Text'])):
            # Don't trigger voice mode if typing in an input field
            return
        
        # Prevent default space behavior and toggle voice mode
        self.toggle_voice_mode()
        return "break"  # Prevent default space handling
    
    def show_help(self, event=None):
        """Show help dialog when F1 is pressed"""
        self.notebook.select(0)  # Switch to chat tab
        help_message = self.get_enhanced_help_message()
        self.add_message("AIVI", help_message, "assistant")
        # Speak a brief help summary
        brief_help = "Help activated. All AIVI features are now displayed in the chat. You can use academic tools, accessibility features, study planner, and voice commands."
        safe_tts_speak(brief_help)
        return "break"
    
    def stop_voice_mode(self, event=None):
        """Stop voice mode when Escape is pressed"""
        if self.is_listening:
            self.toggle_voice_mode()
        else:
            # Speak feedback even if voice mode wasn't active
            safe_tts_speak("Voice mode is already off.")
        return "break"
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Quick access toolbar
        self.create_quick_access_toolbar(main_frame)
        
        # Content area with notebook (tabs)
        self.create_notebook(main_frame)
        
        # Floating action buttons
        self.create_floating_action_buttons()
        
        # Footer with status
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="AIVI", 
                              font=('Segoe UI', 36, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg'])
        title_label.pack(side='left', pady=20)
        
        subtitle_label = tk.Label(header_frame,
                                 text="AI Assistant for Education & Accessibility",
                                 font=('Segoe UI', 14, 'bold'),
                                 fg=self.colors['text'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(side='left', padx=(20, 0), pady=25)
        
        # Control buttons
        controls_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        controls_frame.pack(side='right', pady=20)
        
        # Voice toggle button
        self.voice_btn = tk.Button(controls_frame,
                                  text="🎤 Start Voice",
                                  command=self.toggle_voice_mode,
                                  bg=self.colors['accent'],
                                  fg=self.colors['button_text'],
                                  font=('Segoe UI', 11, 'bold'),
                                  border=2,
                                  relief='solid',
                                  padx=25,
                                  pady=12,
                                  cursor='hand2',
                                  activebackground=self.colors['accent_hover'],
                                  activeforeground=self.colors['button_text'])
        self.voice_btn.pack(side='right', padx=(10, 0))
        
        # Mode toggle button
        mode_text = "🌐 Online" if not self.is_offline_mode else "📱 Offline"
        mode_color = self.colors['success'] if not self.is_offline_mode else self.colors['warning']
        self.mode_btn = tk.Button(controls_frame,
                                 text=mode_text,
                                 command=self.toggle_mode,
                                 bg=mode_color,
                                 fg=self.colors['button_text'],
                                 font=('Segoe UI', 11, 'bold'),
                                 border=2,
                                 relief='solid',
                                 padx=25,
                                 pady=12,
                                 cursor='hand2',
                                 activebackground=mode_color,
                                 activeforeground=self.colors['button_text'])
        self.mode_btn.pack(side='right')
    
    def create_quick_access_toolbar(self, parent):
        """Create a responsive quick access toolbar with feature buttons"""
        toolbar_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        toolbar_frame.pack(fill='x', pady=(0, 20))
        
        # Toolbar title
        toolbar_title = tk.Label(toolbar_frame,
                                text="Quick Access",
                                font=('Segoe UI', 12, 'bold'),
                                fg=self.colors['text'],
                                bg=self.colors['card_bg'])
        toolbar_title.pack(pady=(5, 0))
        
        # Buttons container
        buttons_frame = tk.Frame(toolbar_frame, bg=self.colors['card_bg'])
        buttons_frame.pack(fill='both', expand=True, padx=20, pady=(5, 10))
        
        # Store reference for responsive updates
        self.toolbar_buttons_frame = buttons_frame
        
        # Quick access buttons with icons and tooltips
        self.quick_buttons_data = [
            ("🎙️ Voice", "Toggle voice recognition", self.toggle_voice_mode),
            ("📚 Tutor", "Open Q&A tutor", self.open_qa_tutor),
            ("🧮 Math", "Open math solver", self.open_math_solver),
            ("⠠ Braille", "Convert text to Braille", self.open_braille_tool),
            ("🔍 Search", "Search content", self.open_content_search),
            ("📅 Planner", "Study planner", lambda: self.notebook.select(4)),
            ("💼 Word", "Open Microsoft Word", lambda: self.open_desktop_app("word")),
            ("🧮 Calculator", "Open Calculator", lambda: self.open_desktop_app("calculator")),
            ("🌐 Browser", "Open web browser", lambda: self.open_web_browser()),
            ("❓ Help", "Show help", lambda: self.show_help())
        ]
        
        # Initial layout
        self.layout_toolbar_buttons()
        
        # Bind resize event to parent window
        parent.bind('<Configure>', self.on_window_resize)

    def calculate_optimal_columns(self, width):
        """Calculate optimal number of columns based on window width"""
        # Minimum button width (including padding and margins)
        min_button_width = 120
        available_width = width - 40  # Account for padding
        
        # Calculate maximum possible columns
        max_cols = max(1, available_width // min_button_width)
        
        # Ensure we don't exceed the number of buttons
        total_buttons = len(self.quick_buttons_data)
        
        # Find the best column count that creates balanced rows
        optimal_cols = min(max_cols, total_buttons)
        
        # Try to avoid having just one button in the last row
        if total_buttons % optimal_cols == 1 and optimal_cols > 1:
            optimal_cols = max(1, optimal_cols - 1)
        
        return min(optimal_cols, 6)  # Cap at 6 columns for very wide screens

    def layout_toolbar_buttons(self):
        """Layout buttons responsively based on current window size"""
        # Clear existing buttons
        for widget in self.toolbar_buttons_frame.winfo_children():
            widget.destroy()
        
        # Get current window width
        try:
            window_width = self.root.winfo_width()
            if window_width <= 1:  # Window not yet mapped
                window_width = 1200  # Default width
        except:
            window_width = 1200
        
        # Calculate optimal number of columns
        cols_per_row = self.calculate_optimal_columns(window_width)
        
        # Create buttons in a responsive grid layout
        for i, (text, tooltip, command) in enumerate(self.quick_buttons_data):
            btn = tk.Button(self.toolbar_buttons_frame,
                        text=text,
                        command=command,
                        bg=self.colors['accent'],
                        fg=self.colors['button_text'],
                        font=('Segoe UI', 9, 'bold'),
                        border=1,
                        relief='solid',
                        padx=8,
                        pady=5,
                        cursor='hand2',
                        activebackground=self.colors['accent_hover'],
                        activeforeground=self.colors['button_text'])
            
            # Calculate position in responsive grid
            row = i // cols_per_row
            col = i % cols_per_row
            
            btn.grid(row=row, column=col, padx=3, pady=2, sticky='ew')
            
            # Create tooltip
            self.create_tooltip(btn, tooltip)
        
        # Configure column weights for even distribution
        for col in range(cols_per_row):
            self.toolbar_buttons_frame.grid_columnconfigure(col, weight=1)
        
        # Clear any extra column configurations
        for col in range(cols_per_row, 12):  # Clear up to 12 columns
            self.toolbar_buttons_frame.grid_columnconfigure(col, weight=0)

    def on_window_resize(self, event=None):
        """Handle window resize events"""
        if hasattr(self, 'resize_job') and self.resize_job is not None:
            try:
                self.root.after_cancel(self.resize_job)
            except (tk.TclError, ValueError):
                pass  # Job was already cancelled or invalid
            self.resize_job = None
        
        # Debounce resize events to avoid excessive relayouts
        if self.is_running:
            self.resize_job = self.root.after(100, self.layout_toolbar_buttons)

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, 
                            text=text,
                            background="#ffffe0",
                            foreground="#000000",
                            font=('Segoe UI', 8),
                            relief="solid",
                            borderwidth=1,
                            padx=4,
                            pady=2)
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def create_notebook(self, parent):
        """Create the main tabbed interface"""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_chat_tab()
        self.create_academic_tab()
        self.create_tools_tab()
        self.create_desktop_tab()
        self.create_study_tab()
        self.create_settings_tab()
    
    def create_floating_action_buttons(self):
        """Create floating action buttons for quick access to essential features"""
        # Create floating panel
        self.floating_panel = tk.Frame(self.root, bg=self.colors['card_bg'], relief='solid', bd=2)
        self.floating_panel.place(relx=0.98, rely=0.5, anchor='e')
        
        # Panel title
        panel_title = tk.Label(self.floating_panel,
                              text="Quick Actions",
                              font=('Segoe UI', 10, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'])
        panel_title.pack(pady=(10, 5))
        
        # Essential action buttons
        essential_actions = [
            ("🎤", "Voice", self.toggle_voice_mode, self.colors['success']),
            ("📚", "Tutor", self.open_qa_tutor, self.colors['accent']),
            ("🧮", "Math", self.open_math_solver, self.colors['accent']),
            ("�", "Word", lambda: self.open_desktop_app("word"), self.colors['success']),
            ("🔧", "Calc", lambda: self.open_desktop_app("calculator"), self.colors['success']),
            ("🌐", "Web", lambda: self.open_web_browser(), self.colors['success']),
            ("❓", "Help", lambda: self.show_help(), self.colors['warning'])
        ]
        
        for icon, text, command, color in essential_actions:
            btn_frame = tk.Frame(self.floating_panel, bg=self.colors['card_bg'])
            btn_frame.pack(pady=2, padx=10)
            
            btn = tk.Button(btn_frame,
                           text=icon,
                           command=command,
                           bg=color,
                           fg=self.colors['button_text'],
                           font=('Segoe UI', 16, 'bold'),
                           border=1,
                           relief='solid',
                           width=3,
                           height=1,
                           cursor='hand2',
                           activebackground=self.colors['accent_hover'],
                           activeforeground=self.colors['button_text'])
            btn.pack()
            
            # Label
            label = tk.Label(btn_frame,
                           text=text,
                           font=('Segoe UI', 8),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['card_bg'])
            label.pack()
        
        # Toggle button to show/hide panel
        self.toggle_panel_btn = tk.Button(self.root,
                                         text="◀",
                                         command=self.toggle_floating_panel,
                                         bg=self.colors['accent'],
                                         fg=self.colors['button_text'],
                                         font=('Segoe UI', 12, 'bold'),
                                         border=1,
                                         relief='solid',
                                         width=2,
                                         height=1,
                                         cursor='hand2')
        self.toggle_panel_btn.place(relx=0.95, rely=0.5, anchor='e')
        
        self.floating_panel_visible = True
    
    def toggle_floating_panel(self):
        """Toggle the visibility of the floating action panel"""
        if self.floating_panel_visible:
            self.floating_panel.place_forget()
            self.toggle_panel_btn.config(text="▶")
            self.toggle_panel_btn.place(relx=0.99, rely=0.5, anchor='e')
            self.floating_panel_visible = False
        else:
            self.floating_panel.place(relx=0.98, rely=0.5, anchor='e')
            self.toggle_panel_btn.config(text="◀")
            self.toggle_panel_btn.place(relx=0.95, rely=0.5, anchor='e')
            self.floating_panel_visible = True
    
    def create_chat_tab(self):
        """Create the main chat/interaction tab"""
        chat_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(chat_frame, text='💬 Chat')
        
        # Header with status
        header_frame = tk.Frame(chat_frame, bg=self.colors['accent'], height=60)
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)

        # Title and status
        title_label = tk.Label(header_frame,
                              text="💬 AIVI Chat Assistant",
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['accent'],
                              fg=self.colors['button_text'])
        title_label.pack(side='left', padx=20, pady=15)

        # Status indicator
        self.chat_status = tk.Label(header_frame,
                                   text="🟢 Ready",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['accent'],
                                   fg=self.colors['button_text'])
        self.chat_status.pack(side='right', padx=20, pady=15)

        # Chat display
        chat_container = tk.Frame(chat_frame, bg=self.colors['card_bg'], relief='flat', bd=1)
        chat_container.pack(fill='both', expand=True, padx=20, pady=(5, 20))
        
        # Chat history
        self.chat_display = scrolledtext.ScrolledText(chat_container,
                                                     bg=self.colors['input_bg'],
                                                     fg=self.colors['text'],
                                                     font=('Segoe UI', 12, 'bold'),
                                                     wrap='word',
                                                     border=2,
                                                     relief='solid',
                                                     highlightbackground=self.colors['border'],
                                                     highlightcolor=self.colors['accent'],
                                                     highlightthickness=2,
                                                     padx=20,
                                                     pady=20)
        self.chat_display.pack(fill='both', expand=True, padx=20, pady=(20, 10))
        
        # Input area
        input_frame = tk.Frame(chat_container, bg=self.colors['card_bg'])
        input_frame.pack(fill='x', padx=20, pady=(0, 20))

        # Input field frame
        input_row = tk.Frame(input_frame, bg=self.colors['card_bg'])
        input_row.pack(fill='x', pady=(0, 10))

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_row,
                                   textvariable=self.input_var,
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['input_bg'],
                                   fg=self.colors['text'],
                                   insertbackground=self.colors['accent'],
                                   border=2,
                                   relief='solid',
                                   highlightbackground=self.colors['accent'],
                                   highlightcolor=self.colors['accent'],
                                   highlightthickness=2)
        self.input_entry.pack(side='left', fill='x', expand=True, padx=(0, 15), ipady=10)

        # Large prominent send button
        self.send_btn = tk.Button(input_row,
                                 text="🚀 SEND COMMAND",
                                 command=self.send_message,  # Use original send_message for now
                                 bg='#4CAF50',
                                 fg='white',
                                 font=('Segoe UI', 14, 'bold'),
                                 relief='raised',
                                 padx=20,
                                 pady=12)
        self.send_btn.pack(side='right')

        # Bind keyboard shortcuts
        self.input_entry.bind('<Return>', self.send_message)
        self.input_entry.bind('<Escape>', lambda e: self.input_var.set(""))

        # Command history
        self.command_history = []
        self.history_index = -1

        # Add typing indicator
        self.typing_indicator = tk.Label(input_frame,
                                        text="",
                                        font=('Segoe UI', 10, 'italic'),
                                        bg=self.colors['card_bg'],
                                        fg=self.colors['text'])
        self.typing_indicator.pack(anchor='w', pady=(5, 0))

        # Add command suggestions
        self.suggestions_var = tk.StringVar()
        self.suggestions_label = tk.Label(input_frame,
                                         textvariable=self.suggestions_var,
                                         font=('Segoe UI', 9, 'italic'),
                                         bg=self.colors['card_bg'],
                                         fg=self.colors['accent'],
                                         anchor='w')
        self.suggestions_label.pack(fill='x', pady=(5, 0))

        # Bind input change for real-time suggestions
        self.input_var.trace('w', self.update_suggestions)

        # Add help text for shortcuts
        help_frame = tk.Frame(chat_container, bg=self.colors['card_bg'])
        help_frame.pack(fill='x', padx=20, pady=(0, 10))

        help_text = tk.Label(help_frame,
                            text="💡 Shortcuts: Enter=Send | Esc=Clear | ↑↓=History | Ctrl+Enter=New Line",
                            font=('Segoe UI', 8, 'italic'),
                            bg=self.colors['card_bg'],
                            fg=self.colors['text'],
                            anchor='w')
        help_text.pack(side='left')
        
        # Load voice settings
        self.load_voice_settings()

        # Initialize offline voice control
        self.offline_voice_active = False

        # Add welcome message
        self.add_message("AIVI", "Welcome! I'm your AI assistant. How can I help you today?", "assistant")
    
    def create_academic_tab(self):
        """Create the academic tools tab"""
        academic_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(academic_frame, text='🎓 Academic')

        # Create scrollable frame for academic tools
        canvas = tk.Canvas(academic_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(academic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create grid of academic tools
        tools_grid = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        tools_grid.pack(fill='both', expand=True, padx=20, pady=20)

        # Configure grid weights for proper expansion
        tools_grid.grid_columnconfigure(0, weight=1)
        tools_grid.grid_columnconfigure(1, weight=1)

        academic_tools = [
            ("📚 Q&A Tutoring", "Ask questions and get detailed explanations", self.open_qa_tutor),
            ("🧮 Math Solver", "Solve mathematical problems and formulas", self.open_math_solver),
            ("🔍 Content Search", "Search for academic content", self.open_content_search),
            ("❓ Quiz Mode", "Test your knowledge with quizzes", self.start_quiz_mode),
            ("💡 Academic Counseling", "Get academic advice and guidance", self.open_academic_counsel)
        ]

        for i, (title, description, command) in enumerate(academic_tools):
            row = i // 2
            col = i % 2
            tools_grid.grid_rowconfigure(row, weight=1)
            self.create_tool_card(tools_grid, title, description, command, row, col)
    
    def create_tools_tab(self):
        """Create the accessibility tools tab"""
        tools_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tools_frame, text='🔧 Tools')

        # Create scrollable frame for accessibility tools
        canvas = tk.Canvas(tools_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tools_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create grid of accessibility tools
        tools_grid = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        tools_grid.pack(fill='both', expand=True, padx=20, pady=20)

        # Configure grid weights for proper expansion
        tools_grid.grid_columnconfigure(0, weight=1)
        tools_grid.grid_columnconfigure(1, weight=1)

        accessibility_tools = [
            ("📄 PDF Reader", "Upload and read PDF documents aloud", self.open_pdf_reader),
            ("🎤 Offline Voice Control", "Voice commands without internet", self.open_offline_voice_control),
            ("⠠ Braille Converter", "Convert text to/from Braille", self.open_braille_tool),
            ("🎯 Multi-Modal Input", "Use multiple input methods", self.open_multimodal),
            ("📖 Academic Search", "Search using OpenAI with offline knowledge base", self.open_academic_search)
        ]

        for i, (title, description, command) in enumerate(accessibility_tools):
            row = i // 2
            col = i % 2
            tools_grid.grid_rowconfigure(row, weight=1)
            self.create_tool_card(tools_grid, title, description, command, row, col)

    
    
    def create_desktop_tab(self):
        """Create the desktop control tab"""
        desktop_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(desktop_frame, text='🖥️ Desktop')
        
        # Main container with scrollable area
        main_container = tk.Frame(desktop_frame, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title section
        title_frame = tk.Frame(main_container, bg=self.colors['bg'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame,
                              text="Desktop Control Center",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg'])
        title_label.pack(side='left')
        
        subtitle_label = tk.Label(title_frame,
                                 text="Control your desktop applications and system tools",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(side='left', padx=(20, 0), pady=(10, 0))
        
        # Create scrollable content
        canvas = tk.Canvas(main_container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Applications Section
        self.create_desktop_section(scrollable_frame, "Microsoft Office", [
            ("📄 Word", "Microsoft Word", lambda: self.open_desktop_app("word")),
            ("📊 PowerPoint", "Microsoft PowerPoint", lambda: self.open_desktop_app("powerpoint")),
            ("📈 Excel", "Microsoft Excel", lambda: self.open_desktop_app("excel")),
            ("📓 OneNote", "Microsoft OneNote", lambda: self.open_desktop_app("onenote"))
        ])
        
        self.create_desktop_section(scrollable_frame, "System Tools", [
            ("🔧 Calculator", "Windows Calculator", lambda: self.open_desktop_app("calculator")),
            ("📝 Notepad", "Windows Notepad", lambda: self.open_desktop_app("notepad")),
            ("📋 WordPad", "Windows WordPad", lambda: self.open_desktop_app("wordpad")),
            ("⚙️ Control Panel", "Windows Control Panel", lambda: self.open_desktop_app("control_panel")),
            ("📋 Task Manager", "Windows Task Manager", lambda: self.open_desktop_app("task_manager")),
            ("🔌 Device Manager", "Windows Device Manager", lambda: self.open_desktop_app("device_manager"))
        ])

        # Check admin status and inform user about elevation requirements
        try:
            import ai_assistant.desktop_control as desktop_control
            admin_status = desktop_control.get_elevation_help()
            if "❌" in admin_status:
                # Add admin status info to the chat once
                self.add_message("AIVI", f"ℹ️ Administrator Status:\n{admin_status}", "assistant")
        except Exception:
            pass  # Silent fail if desktop_control not available

        self.create_desktop_section(scrollable_frame, "Web Browsers", [
            ("🌐 Chrome", "Google Chrome", lambda: self.open_desktop_app("chrome")),
            ("🔥 Firefox", "Mozilla Firefox", lambda: self.open_desktop_app("firefox")),
            ("🌊 Edge", "Microsoft Edge", lambda: self.open_desktop_app("edge"))
        ])
        
        self.create_desktop_section(scrollable_frame, "File Explorer", [
            ("📁 Home Folder", "Open Home Directory", lambda: self.open_file_location(None)),
            ("📄 Documents", "Open Documents Folder", lambda: self.open_file_location("Documents")),
            ("⬇️ Downloads", "Open Downloads Folder", lambda: self.open_file_location("Downloads")),
            ("🖥️ Desktop", "Open Desktop Folder", lambda: self.open_file_location("Desktop")),
            ("🖼️ Pictures", "Open Pictures Folder", lambda: self.open_file_location("Pictures")),
            ("🎵 Music", "Open Music Folder", lambda: self.open_file_location("Music")),
            ("🎬 Videos", "Open Videos Folder", lambda: self.open_file_location("Videos"))
        ])
        
        self.create_desktop_section(scrollable_frame, "Quick Web Access", [
            ("🔍 Google", "Open Google Search", lambda: self.open_web_browser("google.com")),
            ("📺 YouTube", "Open YouTube", lambda: self.open_web_browser("youtube.com")),
            ("🔍 Academic Resources", "Search academic resources", self.open_academic_search),
            ("💼 Outlook", "Open Outlook Web", lambda: self.open_web_browser("outlook.com")),
            ("📧 Gmail", "Open Gmail", lambda: self.open_web_browser("gmail.com")),
            ("💻 GitHub", "Open GitHub", lambda: self.open_web_browser("github.com"))
        ])
        
        # Pack the scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_desktop_section(self, parent, section_title, buttons):
        """Create a section of desktop control buttons"""
        section_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief='flat', bd=1)
        section_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        # Section header
        header_frame = tk.Frame(section_frame, bg=self.colors['accent'], height=40)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        section_label = tk.Label(header_frame,
                               text=section_title,
                               font=('Segoe UI', 16, 'bold'),
                               fg=self.colors['button_text'],
                               bg=self.colors['accent'])
        section_label.pack(pady=10)
        
        # Buttons grid
        buttons_grid = tk.Frame(section_frame, bg=self.colors['card_bg'])
        buttons_grid.pack(fill='x', padx=20, pady=(0, 20))
        
        # Create buttons in rows of 3
        for i, (icon_text, description, command) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn_frame = tk.Frame(buttons_grid, bg=self.colors['card_bg'])
            btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Configure column weights
            buttons_grid.grid_columnconfigure(col, weight=1)
            
            # Main button
            btn = tk.Button(btn_frame,
                           text=icon_text,
                           command=command,
                           bg=self.colors['success'],
                           fg=self.colors['button_text'],
                           font=('Segoe UI', 12, 'bold'),
                           border=2,
                           relief='solid',
                           padx=15,
                           pady=10,
                           cursor='hand2',
                           activebackground=self.colors['accent_hover'],
                           activeforeground=self.colors['button_text'],
                           width=20)
            btn.pack(fill='x', pady=(0, 5))
            
            # Description label
            desc_label = tk.Label(btn_frame,
                                text=description,
                                font=('Segoe UI', 9),
                                fg=self.colors['text_secondary'],
                                bg=self.colors['card_bg'],
                                wraplength=180)
            desc_label.pack()
    
    def open_desktop_app(self, app_name):
        """Open a desktop application"""
        try:
            import ai_assistant.desktop_control as desktop_control
            success, message = desktop_control.open_app(app_name)
            
            # Show result in chat
            self.notebook.select(0)  # Switch to chat tab
            if success:
                self.add_message("AIVI", f"✅ {message}", "assistant")
                self.update_status(f"Opened {app_name}", "success")
                safe_tts_speak(f"Successfully opened {app_name.replace('_', ' ')}")
            else:
                self.add_message("AIVI", f"❌ {message}", "assistant")
                self.update_status(f"Failed to open {app_name}", "error")
                safe_tts_speak(f"Failed to open {app_name.replace('_', ' ')}: {message}")
                
        except Exception as e:
            error_msg = f"Error opening {app_name}: {str(e)}"
            self.add_message("AIVI", f"❌ {error_msg}", "assistant")
            self.update_status(error_msg, "error")
            safe_tts_speak(error_msg)

    def open_file_location(self, folder_name):
        """Open a file location"""
        try:
            import ai_assistant.desktop_control as desktop_control
            
            if folder_name:
                path = os.path.expanduser(f"~/{folder_name}")
            else:
                path = None
                
            success, message = desktop_control.open_file_explorer(path)
            
            # Show result in chat
            self.notebook.select(0)  # Switch to chat tab
            if success:
                self.add_message("AIVI", f"✅ {message}", "assistant")
                location = folder_name if folder_name else "Home"
                self.update_status(f"Opened {location} folder", "success")
                safe_tts_speak(f"Opened {location} folder")
            else:
                self.add_message("AIVI", f"❌ {message}", "assistant")
                self.update_status(f"Failed to open folder", "error")
                safe_tts_speak(f"Failed to open folder: {message}")
                
        except Exception as e:
            error_msg = f"Error opening folder: {str(e)}"
            self.add_message("AIVI", f"❌ {error_msg}", "assistant")
            self.update_status(error_msg, "error")
            safe_tts_speak(error_msg)
    
    def open_web_browser(self, url=None):
        """Open web browser with optional URL"""
        try:
            import ai_assistant.desktop_control as desktop_control
            
            if url:
                success, message = desktop_control.open_website(url)
                action = f"Opened {url}"
                speech = f"Opened {url.replace('.com', '').replace('.org', '')}"
            else:
                success, message = desktop_control.open_website("google.com")
                action = "Opened browser"
                speech = "Opened web browser"
            
            # Show result in chat
            self.notebook.select(0)  # Switch to chat tab
            if success:
                self.add_message("AIVI", f"✅ {message}", "assistant")
                self.update_status(action, "success")
                safe_tts_speak(speech)
            else:
                self.add_message("AIVI", f"❌ {message}", "assistant")
                self.update_status("Failed to open browser", "error")
                safe_tts_speak(f"Failed to open browser: {message}")
                
        except Exception as e:
            error_msg = f"Error opening browser: {str(e)}"
            self.add_message("AIVI", f"❌ {error_msg}", "assistant")
            self.update_status(error_msg, "error")
            safe_tts_speak(error_msg)
    
    def create_study_tab(self):
        """Create the study planner tab"""
        study_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(study_frame, text='📅 Study Planner')
        
        # Study planner interface
        planner_container = tk.Frame(study_frame, bg=self.colors['card_bg'], relief='flat', bd=1)
        planner_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(planner_container,
                              text="Study Planner & Reminders",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'])
        title_label.pack(pady=20)
        
        # Event input
        event_frame = tk.Frame(planner_container, bg=self.colors['card_bg'])
        event_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(event_frame, text="Add Event:", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'], 
                bg=self.colors['card_bg']).pack(anchor='w')
        
        self.event_entry = tk.Entry(event_frame,
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['input_bg'],
                                   fg=self.colors['text'],
                                   insertbackground=self.colors['accent'],
                                   border=2,
                                   relief='solid',
                                   highlightbackground=self.colors['border'],
                                   highlightcolor=self.colors['accent'],
                                   highlightthickness=2)
        self.event_entry.pack(fill='x', pady=(5, 0), ipady=10)
        
        tk.Button(event_frame,
                 text="Add Event",
                 command=self.add_study_event,
                 bg=self.colors['accent'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 cursor='hand2',
                 activebackground=self.colors['accent_hover'],
                 activeforeground=self.colors['button_text']).pack(pady=15)
        
        # Reminder input
        reminder_frame = tk.Frame(planner_container, bg=self.colors['card_bg'])
        reminder_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(reminder_frame, text="Set Reminder:", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'], 
                bg=self.colors['card_bg']).pack(anchor='w')
        
        self.reminder_entry = tk.Entry(reminder_frame,
                                      font=('Segoe UI', 12, 'bold'),
                                      bg=self.colors['input_bg'],
                                      fg=self.colors['text'],
                                      insertbackground=self.colors['accent'],
                                      border=2,
                                      relief='solid',
                                      highlightbackground=self.colors['border'],
                                      highlightcolor=self.colors['accent'],
                                      highlightthickness=2)
        self.reminder_entry.pack(fill='x', pady=(5, 0), ipady=10)
        
        tk.Button(reminder_frame,
                 text="Set Reminder",
                 command=self.set_study_reminder,
                 bg=self.colors['success'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 cursor='hand2',
                 activebackground=self.colors['success'],
                 activeforeground=self.colors['button_text']).pack(pady=15)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(settings_frame, text='⚙️ Settings')
        
        settings_container = tk.Frame(settings_frame, bg=self.colors['card_bg'], relief='flat', bd=1)
        settings_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(settings_container,
                              text="Settings & Preferences",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'])
        title_label.pack(pady=20)
        
        # Voice settings
        voice_section = tk.Frame(settings_container, bg=self.colors['card_bg'])
        voice_section.pack(fill='x', padx=20, pady=10)
        
        tk.Label(voice_section, text="Voice Settings:", 
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'], 
                bg=self.colors['card_bg']).pack(anchor='w')
        
        voice_options = ['Default', 'Male', 'Female', 'Custom']
        self.voice_var = tk.StringVar(value='Default')
        
        for option in voice_options:
            tk.Radiobutton(voice_section,
                          text=option,
                          variable=self.voice_var,
                          value=option,
                          bg=self.colors['card_bg'],
                          fg=self.colors['text'],
                          selectcolor=self.colors['accent'],
                          activebackground=self.colors['card_bg'],
                          activeforeground=self.colors['text'],
                          font=('Segoe UI', 11)).pack(anchor='w', padx=20)
        
        # Apply voice settings button
        tk.Button(voice_section,
                 text="Apply Voice Settings",
                 command=self.apply_voice_settings,
                 bg=self.colors['accent'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 cursor='hand2',
                 activebackground=self.colors['accent_hover'],
                 activeforeground=self.colors['button_text']).pack(pady=15, anchor='w')

    
    def create_tool_card(self, parent, title, description, command, row, col):
        """Create a tool card widget"""
        # Create card frame with visual styling
        card = tk.Frame(parent,
                       bg=self.colors['card_bg'],
                       relief='solid',
                       bd=2,
                       highlightbackground=self.colors['border'],
                       highlightthickness=1,
                       width=300,
                       height=200)
        card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew', ipadx=10, ipady=10)

        # Prevent the frame from shrinking
        card.grid_propagate(False)

        # Configure grid weights for proper expansion
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)

        # Title with larger font and better spacing
        title_label = tk.Label(card,
                             text=title,
                             font=('Segoe UI', 18, 'bold'),
                             fg=self.colors['text'],
                             bg=self.colors['card_bg'],
                             anchor='center')
        title_label.pack(pady=(25, 12), fill='x')

        # Description with better wrapping
        desc_label = tk.Label(card,
                            text=description,
                            font=('Segoe UI', 12),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['card_bg'],
                            wraplength=250,
                            justify='center',
                            anchor='center')
        desc_label.pack(pady=(0, 20), fill='x', padx=10)

        # Button with enhanced styling
        btn = tk.Button(card,
                       text="✨ Open Tool",
                       command=command,
                       bg=self.colors['accent'],
                       fg=self.colors['button_text'],
                       font=('Segoe UI', 12, 'bold'),
                       border=0,
                       relief='flat',
                       padx=30,
                       pady=12,
                       cursor='hand2',
                       activebackground=self.colors['accent_hover'],
                       activeforeground=self.colors['button_text'])
        btn.pack(pady=(0, 25), padx=20, fill='x')

        # Add hover effect
        def on_enter(e):
            btn.configure(bg=self.colors['accent_hover'])

        def on_leave(e):
            btn.configure(bg=self.colors['accent'])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def create_footer(self, parent):
        """Create the footer with status bar"""
        self.footer_frame = tk.Frame(parent, bg=self.colors['card_bg'], height=50)
        self.footer_frame.pack(fill='x', pady=(20, 0))
        self.footer_frame.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(self.footer_frame,
                                   text="Ready",
                                   font=('Segoe UI', 10),
                                   fg=self.colors['text'],
                                   bg=self.colors['card_bg'])
        self.status_label.pack(side='left', padx=20, pady=15)
        
        # Search mode indicator
        self.search_mode_label = tk.Label(self.footer_frame,
                                        text=f"Search: {self.search_mode.replace('_', ' ').title()}",
                                        font=('Segoe UI', 9),
                                        fg=self.colors['text_secondary'],
                                        bg=self.colors['card_bg'])
        self.search_mode_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Current time
        self.time_label = tk.Label(self.footer_frame,
                                 text="",
                                 font=('Segoe UI', 10),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['card_bg'])
        self.time_label.pack(side='right', padx=20, pady=15)
        
        self.update_time()
    
    def update_time(self):
        """Update the time display"""
        if not self.is_running:
            return
            
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=current_time)
            # Store the job reference for cleanup
            self.timer_job = self.root.after(1000, self.update_time)
        except tk.TclError:
            # Widget destroyed, stop updating
            self.is_running = False
    
    def update_status(self, message, status_type="info"):
        """Update the status bar"""
        colors = {
            'info': self.colors['text'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'error': self.colors['error']
        }
        self.status_label.config(text=message, fg=colors.get(status_type, self.colors['text']))
    
    def update_search_mode_display(self):
        """Update the search mode indicator"""
        try:
            if hasattr(self, 'search_mode_label'):
                mode_display = self.search_mode.replace('_', ' ').title()
                self.search_mode_label.config(text=f"Search: {mode_display}")
        except Exception as e:
            print(f"Error updating search mode display: {e}")
    
    def add_message(self, sender, message, msg_type="user"):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Format message
        if msg_type == "assistant":
            formatted_msg = f"[{timestamp}] 🤖 {sender}: {message}\n\n"
            color = self.colors['accent']
        else:
            formatted_msg = f"[{timestamp}] 👤 You: {message}\n\n"
            color = self.colors['success']
        
        # Insert message
        self.chat_display.insert(tk.END, formatted_msg)
        self.chat_display.see(tk.END)
        
        # Auto-scroll
        self.chat_display.update()
    
    def enhanced_send_message(self, event=None):
        """Enhanced send message with better feedback and validation"""
        message = self.input_var.get().strip()
        if not message:
            self.shake_input()
            return

        # Disable send button while processing
        self.send_btn.config(state='disabled', text="⏳ PROCESSING...", bg='#ff9800')

        # Clear suggestions
        self.suggestions_var.set("")

        # Add to command history
        if message not in self.command_history:
            self.command_history.append(message)
        self.history_index = -1

        # Add user message
        self.add_message("You", message, "user")
        self.input_var.set("")

        # Show typing indicator
        self.show_typing_indicator()

        # Process command in separate thread
        threading.Thread(target=self.enhanced_process_command, args=(message,), daemon=True).start()

    def send_message(self, event=None):
        """Handle sending a message (legacy compatibility)"""
        return self.enhanced_send_message(event)

    def shake_input(self):
        """Visual feedback for empty input"""
        original_bg = self.input_entry.cget('bg')
        self.input_entry.config(bg='#ffcccc')
        self.root.after(200, lambda: self.input_entry.config(bg=original_bg))

    def show_typing_indicator(self):
        """Show typing indicator while processing"""
        self.typing_indicator.config(text="🤖 AIVI is typing...")
        self.chat_status.config(text="🟡 Processing...", fg='yellow')

    def hide_typing_indicator(self):
        """Hide typing indicator"""
        self.typing_indicator.config(text="")
        self.chat_status.config(text="🟢 Ready", fg=self.colors['button_text'])

    def update_suggestions(self, *args):
        """Update command suggestions based on input"""
        current_text = self.input_var.get().lower()
        if len(current_text) < 2:
            self.suggestions_var.set("")
            return

        suggestions = []
        common_commands = [
            "help", "features", "voice settings", "open camera", "open calculator",
            "open notepad", "open settings", "take screenshot", "read this",
            "what time is it", "weather", "translate", "math help"
        ]

        for cmd in common_commands:
            if current_text in cmd.lower():
                suggestions.append(cmd)

        if suggestions:
            suggestion_text = f"💡 Try: {', '.join(suggestions[:3])}"
            self.suggestions_var.set(suggestion_text)
        else:
            self.suggestions_var.set("")

    def enhanced_process_command(self, command):
        """Enhanced command processing with better feedback"""
        try:
            # Process the command using existing logic
            self.process_command(command)
        finally:
            # Re-enable send button and hide indicators
            self.root.after(0, self.reset_send_button)
            self.root.after(0, self.hide_typing_indicator)

    def reset_send_button(self):
        """Reset send button to normal state"""
        self.send_btn.config(state='normal', text="🚀 SEND COMMAND", bg='#4CAF50')

    def clear_input(self, event=None):
        """Clear the input field"""
        self.input_var.set("")
        self.suggestions_var.set("")

    def previous_command(self, event=None):
        """Navigate to previous command in history"""
        if not self.command_history:
            return

        if self.history_index == -1:
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1

        if 0 <= self.history_index < len(self.command_history):
            self.input_var.set(self.command_history[self.history_index])

    def next_command(self, event=None):
        """Navigate to next command in history"""
        if not self.command_history or self.history_index == -1:
            return

        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_var.set(self.command_history[self.history_index])
        else:
            self.history_index = -1
            self.input_var.set("")
    
    def process_command(self, command):
        """Process user command and generate response with enhanced desktop control and conversation"""
        try:
            command_lower = command.lower()
            response = ""
            
            # First, try desktop control commands (if voice_commands is available)
            if voice_commands is not None:
                success, desktop_message, action = voice_commands.process_desktop_command(command)
                if success:
                    response = desktop_message
                    self.update_status(f"Desktop action: {action}", "success")
                elif action != "no_action":
                    # Command was recognized as desktop command but failed
                    response = desktop_message
            else:
                success, desktop_message, action = False, "", "no_action"
            
            if not success and action == "no_action":
                # Not a desktop command, proceed with existing logic
                
                # Get conversation context for better AI responses (if voice_commands available)
                if voice_commands is not None:
                    context = voice_commands.get_conversation_context(command)
                else:
                    context = {'intent': 'unknown', 'entities': [], 'emotion': 'neutral', 'urgency': 'normal', 'topic': None}
                
                # Use offline conversation AI for natural responses
                if self.is_offline_mode:
                    response = offline_conversation.chat_with_ai(command, context)
                else:
                    # Online mode - use existing command processing with enhancements
                    
                    # Help/Features List (enhanced)
                    if command_lower in ["help", "features", "commands", "what can you do", "menu"]:
                        response = self.get_enhanced_help_message()
                    
                    # Desktop Control Commands (new)
                    elif any(word in command_lower for word in ["open", "start", "launch", "run"]):
                        # This is handled above by desktop control, but provide fallback
                        if "application" in command_lower or "app" in command_lower:
                            available_apps = desktop_control.get_available_applications()
                            app_list = ", ".join(available_apps.keys())
                            response = f"Available applications: {app_list}. Say 'open [app name]' to launch an application."
                        else:
                            response = "I can help you open applications, websites, or folders. What would you like to open?"
                    
                    # Natural Conversation (enhanced)
                    elif any(word in command_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
                        response = "Hello! I'm AIVI, your AI assistant for education and accessibility. I can help you with studies, open applications, answer questions, and much more. What would you like to do today?"
                    
                    # Academic Counselling (enhanced)
                    elif any(x in command_lower for x in ["counsel", "advice", "guidance"]):
                        if "search online" in command_lower or "online" in command_lower:
                            desktop_control.open_website("google.com/search?q=academic+counselling+resources")
                            response = "I have opened online resources for academic counselling in your browser."
                        else:
                            response = offline_academic.offline_search("academic counselling")
                            response += "\n\nI'm also here to provide personal guidance. What specific academic challenge are you facing?"
                    
                    # Tutor/QA (enhanced with conversation context)
                    elif any(x in command_lower for x in ["tutor", "question", "explain", "define", "what is", "who is", "how do", "when is", "why"]):
                        # Use both QA tutoring and conversation AI
                        qa_response = qa_tutoring.answer_question(command)
                        conversation_response = offline_conversation.chat_with_ai(command, context)
                        
                        # Combine responses intelligently
                        if "I don't have specific information" in qa_response or len(qa_response) < 50:
                            response = conversation_response
                        else:
                            response = qa_response
                            if context['emotion'] == 'anxious':
                                response += "\n\nDon't worry, take your time to understand this. Would you like me to explain any part in more detail?"
                    
                    # Quiz (enhanced)
                    elif "quiz" in command_lower:
                        response = "Starting quiz mode. I'll ask you questions to test your knowledge."
                        # Switch to Academic tab for quiz interface
                        self.root.after(0, lambda: self.notebook.select(1))
                        try:
                            qa_tutoring.quiz_mode()
                        except:
                            response += " Please use the Academic tab for interactive quiz features."
                        
                        # Add encouragement based on context
                        if context['emotion'] == 'anxious':
                            response += " Remember, quizzes are for learning, not judging. You're doing great!"
                    
                    # Math (enhanced)
                    elif "math" in command_lower or "solve" in command_lower or "formula" in command_lower:
                        if "solve" in command_lower:
                            # Extract problem from command
                            problem = command_lower.replace("solve", "").strip()
                            if problem:
                                try:
                                    solution = math_reader.solve_math_problem(problem)
                                    response = f"Solution: {solution}"
                                    
                                    # Add encouraging response
                                    if context['emotion'] == 'anxious':
                                        response += "\n\nMath can be challenging, but you're doing well by asking for help!"
                                except Exception as e:
                                    response = f"I had trouble solving that problem: {str(e)}. Could you rephrase it or break it down into smaller parts?"
                            else:
                                response = "Please tell me the math problem you'd like me to solve. For example, 'solve 2 plus 3' or 'solve x equals 5 plus 2'."
                        elif "formula" in command_lower:
                            # Extract formula from command
                            formula = command_lower.replace("formula", "").strip()
                            if formula:
                                try:
                                    desc = math_reader.read_formula(formula)
                                    response = f"Formula description: {desc}"
                                except Exception as e:
                                    response = f"Could not read formula: {str(e)}"
                            else:
                                response = "Please specify the formula you'd like me to explain."
                        else:
                            self.open_math_solver()
                            response = "Math solver opened. You can enter your problem in the dialog, or just tell me what you need help with."
                    
                    # Braille (enhanced)
                    elif "braille" in command_lower:
                        if "to braille" in command_lower:
                            text_to_convert = command_lower.replace("to braille", "").strip()
                            if text_to_convert:
                                try:
                                    braille_text = braille.text_to_braille(text_to_convert)
                                    response = f"Braille: {braille_text}"
                                except Exception as e:
                                    response = f"Braille conversion error: {str(e)}"
                            else:
                                response = "Please tell me the text you'd like to convert to Braille."
                        elif "to text" in command_lower:
                            braille_to_convert = command_lower.replace("to text", "").strip()
                            if braille_to_convert:
                                try:
                                    text = braille.braille_to_text(braille_to_convert)
                                    response = f"Text: {text}"
                                except Exception as e:
                                    response = f"Braille to text error: {str(e)}"
                            else:
                                response = "Please provide the Braille text you'd like to convert."
                        else:
                            response = "I can convert text to Braille or Braille to text. Say 'convert [text] to braille' or 'convert [braille] to text'."
                    
                    # Study Planner (enhanced)
                    elif "planner" in command_lower or "reminder" in command_lower or "event" in command_lower:
                        if "add event" in command_lower:
                            event_desc = command_lower.replace("add event", "").strip()
                            if event_desc:
                                try:
                                    study_planner.add_event(event_desc)
                                    response = "Event added to your study planner."
                                except Exception as e:
                                    response = f"Could not add event: {str(e)}"
                            else:
                                response = "Please describe the event you'd like to add. For example, 'add event math quiz on Friday'."
                        elif "set reminder" in command_lower:
                            reminder_desc = command_lower.replace("set reminder", "").strip()
                            if reminder_desc:
                                try:
                                    study_planner.set_reminder(reminder_desc)
                                    response = "Reminder set."
                                except Exception as e:
                                    response = f"Could not set reminder: {str(e)}"
                            else:
                                response = "Please describe what you'd like to be reminded about."
                        else:
                            response = "I can help you plan your studies. Say 'add event [description]' or 'set reminder [description]'."
                    
                    # Content Search (enhanced)
                    elif "search" in command_lower:
                        query = command_lower.replace("search", "").strip()
                        if query:
                            offline = os.path.exists("offline_mode.flag")
                            if offline:
                                response = offline_academic.offline_search(query)
                            else:
                                response = content_search.search_content(query)
                        else:
                            response = "What would you like me to search for? I can search academic content, or you can say 'search online for [topic]' to open a web search."
                    
                    # Multi-modal (enhanced)
                    elif "multi modal" in command_lower or "multimodal" in command_lower:
                        response = "Multi-modal input allows you to use voice, text, and other input methods together. What type of input would you like to use?"
                        try:
                            multi_modal.accept_input("speech")  # Default to speech
                            response += " Speech input is now active."
                        except Exception as e:
                            response = f"Multi-modal error: {str(e)}"
                    
                    # Web browsing (enhanced)
                    elif "google" in command_lower:
                        if "search for" in command_lower:
                            query = command_lower.split("search for")[1].strip()
                            desktop_control.open_website(f"google.com/search?q={query.replace(' ', '+')}")
                            response = f"Opened Google search for '{query}' in your browser."
                        else:
                            desktop_control.open_website("google.com")
                            response = "Opened Google in your browser."
                    
                    elif "youtube" in command_lower:
                        if "search for" in command_lower:
                            query = command_lower.split("search for")[1].strip()
                            desktop_control.open_website(f"youtube.com/results?search_query={query.replace(' ', '+')}")
                            response = f"Opened YouTube search for '{query}' in your browser."
                        else:
                            desktop_control.open_website("youtube.com")
                            response = "Opened YouTube in your browser."
                    
                    # Academic search with enhanced offline-first approach
                    elif any(x in command_lower for x in ["scholar", "academic", "research", "paper", "search for", "search"]):
                        query = command_lower.replace("scholar", "").replace("academic", "").replace("research", "").replace("paper", "").replace("search for", "").replace("search", "").strip()
                        if query:
                            # Use enhanced search with offline-first approach
                            response = self.search_enhanced(query)
                        else:
                            response = "What would you like me to search for? I can search offline knowledge, Google, or academic resources."
                    
                    # Offline/Online mode (enhanced)
                    elif "offline" in command_lower:
                        offline_mode.enable_offline_mode()
                        offline_academic.set_mode('offline')
                        self.is_offline_mode = True
                        response = "Offline mode enabled. I'll now use my offline knowledge base for all responses."
                        self.update_status("Offline mode enabled", "warning")
                    
                    elif "online" in command_lower:
                        current_mode = offline_academic.get_mode() if hasattr(offline_academic, 'get_mode') else 'offline'
                        if current_mode == 'offline':
                            try:
                                offline_academic.set_mode('online')
                                self.is_offline_mode = False
                                response = "Online mode enabled. I now have access to web-based resources."
                                self.update_status("Online mode enabled", "success")
                            except:
                                response = "Could not switch to online mode. Staying in offline mode."
                        else:
                            offline_academic.set_mode('online')
                            self.is_offline_mode = False
                            response = "Online mode enabled."
                            self.update_status("Online mode enabled", "success")
                    
                    # Enhanced search mode switching
                    elif any(phrase in command_lower for phrase in ["search mode", "set search mode", "change search mode"]):
                        if "offline first" in command_lower or "offline-first" in command_lower:
                            self.search_mode = "offline_first"
                            self.update_search_mode_display()
                            response = "Search mode set to 'Offline First' - I'll check local knowledge first, then search online if needed."
                        elif "google first" in command_lower or "google-first" in command_lower:
                            self.search_mode = "google_first"
                            self.update_search_mode_display()
                            response = "Search mode set to 'Google First' - I'll search online first, then check local knowledge."
                        elif "ai only" in command_lower or "ai-only" in command_lower:
                            self.search_mode = "ai_only"
                            self.update_search_mode_display()
                            response = "Search mode set to 'AI Only' - I'll use AI-powered responses only."
                        else:
                            response = f"Current search mode: {self.search_mode}. Available modes: 'offline first', 'google first', 'ai only'."
                    
                    # Show current search mode
                    elif "what search mode" in command_lower or "current search mode" in command_lower:
                        mode_descriptions = {
                            "offline_first": "Offline First - checks local knowledge before searching online",
                            "google_first": "Google First - searches online before checking local knowledge",
                            "ai_only": "AI Only - uses AI-powered responses exclusively"
                        }
                        response = f"Current search mode: {mode_descriptions.get(self.search_mode, self.search_mode)}"
                    
                    # Voice Settings commands (updated to avoid system settings conflict)
                    elif "voice settings" in command_lower or "speech settings" in command_lower or "open voice settings" in command_lower:
                        self.root.after(0, self.open_voice_settings)
                        response = "Opening voice and speech settings. You can adjust volume, speed, and voice gender."

                    # Voice mode switching (enhanced)
                    elif "change voice mode" in command_lower or "switch voice mode" in command_lower or "voice mode" in command_lower:
                        if "male" in command_lower:
                            result = tts.set_voice_mode('male')
                            response = "Voice mode changed to male." if result else "Could not change to male voice mode."
                        elif "female" in command_lower:
                            result = tts.set_voice_mode('female')
                            response = "Voice mode changed to female." if result else "Could not change to female voice mode."
                        else:
                            response = "Which voice mode would you like? Say 'male voice', 'female voice', or 'default voice'."
                
                    # Real-time transcription (enhanced)
                    elif "real time transcription" in command_lower or "live transcription" in command_lower:
                        if voice_commands is not None and hasattr(voice_commands, 'start_real_time_transcription'):
                            response = "Starting real-time voice transcription. Say 'stop transcription' to end."
                            try:
                                for transcript in voice_commands.start_real_time_transcription():
                                    if transcript.strip().lower() in ["stop transcription", "stop", "exit"]:
                                        response = "Transcription stopped."
                                        break
                                    # Add transcript to chat
                                    self.root.after(0, lambda t=transcript: self.add_message("Transcription", f"You said: {t}", "user"))
                            except Exception as e:
                                response = f"Real-time transcription error: {str(e)}"
                        else:
                            response = "Real-time transcription is not available. Speech recognition module is not installed."
                    
                    # Knowledge base management commands
                    elif any(phrase in command_lower for phrase in ["show knowledge", "knowledge stats", "knowledge statistics"]):
                        if self.offline_data:
                            stats = self.offline_data.get_statistics()
                            response = f"📚 Knowledge Base Statistics:\n"
                            response += f"• Total entries: {stats.get('total_entries', 0)}\n"
                            response += f"• Topics covered: {stats.get('topics_count', 0)}\n"
                            response += f"• Data sources: {stats.get('sources_count', 0)}\n"
                            response += f"• Last updated: {stats.get('last_updated', 'Unknown')}\n"
                            response += f"• Search cache entries: {stats.get('cache_entries', 0)}"
                        else:
                            response = "Knowledge base is not available. Enhanced offline features are not loaded."
                    
                    elif any(phrase in command_lower for phrase in ["add knowledge", "add to knowledge", "save this knowledge"]):
                        if self.offline_data:
                            # Extract the content after the command
                            for phrase in ["add knowledge", "add to knowledge", "save this knowledge"]:
                                if phrase in command_lower:
                                    content = command[command_lower.find(phrase) + len(phrase):].strip()
                                    break
                            
                            if content:
                                success = self.offline_data.add_knowledge(
                                    topic="User Input",
                                    content=content,
                                    source="manual_entry"
                                )
                                if success:
                                    response = "✅ Knowledge added to the offline database successfully!"
                                else:
                                    response = "❌ Failed to add knowledge to the database."
                            else:
                                response = "What knowledge would you like to add? Please specify after 'add knowledge'."
                        else:
                            response = "Knowledge base is not available. Enhanced offline features are not loaded."
                    
                    # Exit/Quit (enhanced)
                    elif "exit" in command_lower or "quit" in command_lower:
                        # Save conversation before exiting
                        if hasattr(offline_conversation, 'save_session'):
                            offline_conversation.save_session()
                        
                        response = "Thank you for using AIVI! Your conversation has been saved. Goodbye!"
                        safe_tts_speak(response)
                        self.root.after(2000, self.root.quit)  # Close after 2 seconds
                        return
                    
                    # Emotional support and encouragement (new)
                    elif any(word in command_lower for word in ["frustrated", "confused", "difficult", "hard", "struggling"]):
                        response = "I understand this can be challenging. Remember, every expert was once a beginner. Let's work through this together. What specific part would you like help with?"
                    
                    elif any(word in command_lower for word in ["thank", "thanks", "appreciate"]):
                        response = "You're very welcome! I'm here to help anytime. Is there anything else you'd like to work on?"
                    
                    # Default response (enhanced)
                    else:
                        # Try offline conversation AI for natural response
                        response = offline_conversation.chat_with_ai(command, context)
                        
                        # If still no good response, provide helpful guidance
                        if len(response) < 20:
                            response = "I'm here to help! I can assist with studies, open applications, answer questions, provide accessibility features, and much more. What would you like to do? Say 'help' to see all available features."
            
            # Add response to chat
            self.root.after(0, lambda: self.add_message("AIVI", response, "assistant"))
            
            # Automatically learn from conversation (enhanced feature)
            self._learn_from_conversation(command, response)
            
            # Speak the response
            safe_tts_speak(response)
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.root.after(0, lambda: self.add_message("AIVI", error_msg, "assistant"))
            # Speak the error message
            safe_tts_speak(error_msg)
    
    def _learn_from_conversation(self, command, response):
        """Automatically learn from conversations for offline knowledge"""
        try:
            if self.offline_data and len(response) > 50:  # Only learn meaningful responses
                # Skip system messages and errors
                if any(phrase in response.lower() for phrase in ["error", "failed", "not available", "cannot"]):
                    return
                
                # Extract key topic from command
                topic = command[:100] if len(command) > 100 else command
                
                # Add to knowledge base for future offline use
                self.offline_data.add_knowledge(
                    topic=topic.strip(),
                    content=response,
                    source="conversation_learning",
                    metadata={
                        "timestamp": datetime.now().isoformat(),
                        "command_type": "conversation",
                        "response_length": len(response)
                    }
                )
        except Exception as e:
            # Silent fail - learning is optional
            print(f"Learning error (non-critical): {e}")
    
    def get_enhanced_help_message(self):
        """Get the enhanced help/features message with offline-first features"""
        enhanced_status = "✅ Enhanced" if self.offline_data else "⚠ Standard"
        search_mode_display = self.search_mode.replace('_', ' ').title()
        
        return f"""🤖 AIVI - AI Assistant for Education & Accessibility ({enhanced_status} Mode)

📚 ACADEMIC FEATURES:
- Ask questions: "What is photosynthesis?", "Explain algebra", "Define democracy"
- Math solver: "Solve 2 plus 3", "Formula for area of circle"
- Quiz mode: "Start quiz", "Test my knowledge"
- Academic counseling: "I need study advice", "Help with academic planning"

� ENHANCED SEARCH (Current Mode: {search_mode_display}):
- Smart search: "Search for [topic]" - Uses offline-first approach
- Search modes: "Set search mode offline first", "Set search mode google first", "Set search mode ai only"
- Knowledge base: "Show knowledge stats", "Add knowledge [content]"
- Comprehensive results from offline data, Google search, and AI

�💻 DESKTOP CONTROL:
- Open applications: "Open Word", "Start PowerPoint", "Launch Calculator"
- Open folders: "Open documents folder", "Show downloads", "Navigate to desktop"
- Web browsing: "Open Google", "Go to YouTube", "Search for [topic]"
- System tools: "Open control panel", "Start task manager", "Show file explorer"

♿ ACCESSIBILITY FEATURES:
- Text conversion: "Convert to Braille"
- Voice control with beep feedback: Press SPACEBAR or say commands
- Real-time transcription: "Start real-time transcription"

🗺️ NAVIGATION & SEARCH:
- Content search: "Search for [topic]", "Find information about"
- Academic search: "Search academic [topic]", "Research [subject]"
- Offline knowledge: Always available, constantly learning from your searches

📅 ORGANIZATION:
- Study planner: "Add event [description]", "Set reminder [details]"
- Time management: "Schedule study time", "Plan my week"

🎙️ VOICE COMMANDS (Enhanced with Beep Feedback):
- Natural conversation: Just speak naturally, I understand context
- Offline mode: "Switch to offline mode" (uses local knowledge)
- Online mode: "Switch to online mode" (access web resources)
- Listen timeout: 15 seconds with audio feedback

⌨️ KEYBOARD SHORTCUTS:
• SPACEBAR: Toggle enhanced voice mode with beep feedback
• F1: Show this help message
• ESC: Stop voice mode
• ENTER: Send message in chat

💡 ENHANCED TIPS:
- I now learn from every search and save useful information offline
- Three search modes: Offline First (recommended), Google First, AI Only
- Voice commands include audio beep feedback when ready to listen
- All search results are automatically cached for offline use
- Ask "Show knowledge stats" to see how much I've learned

🔧 CURRENT STATUS:
- Search Mode: {search_mode_display}
- Offline Data: {'Available' if self.offline_data else 'Not Available'}
- Voice Manager: {'Enhanced' if self.enhanced_voice_manager else 'Standard'}
- Google Search: {'Available' if self.google_search_manager else 'Not Available'}

Say any command to begin, or ask "What can you help me with?" for specific guidance!"""
    
    def search_academic(self, query, use_openai=True):
        """Search using OpenAI and cache results to offline knowledge base"""
        try:
            # First check offline knowledge base
            if self.offline_data_manager:
                offline_results = self.offline_data_manager.search_offline_data(query)
                if offline_results and offline_results[0].get('confidence', 0) >= 0.85:
                    best_result = offline_results[0]
                    cached_response = f"""📚 From Knowledge Base: "{query}"

{best_result['answer']}

📖 Source: {best_result.get('source', 'AIVI Knowledge Base')}
✅ Confidence: {best_result.get('confidence', 0) * 100:.0f}%"""
                    
                    self.root.after(0, lambda: self.add_message("AIVI", cached_response, "assistant"))
                    safe_tts_speak(f"From knowledge base: {best_result['answer'][:200]}", self)
                    return cached_response
            
            # Use OpenAI if not in cache
            if OpenAI is not None:
                api_key = os.getenv('OPENAI_API_KEY')

                if not api_key or api_key == "your-openai-api-key-here":
                    return "Please set up your OpenAI API key in the .env file to enable academic search."

                try:
                    client = OpenAI(api_key=api_key)

                    prompt = f"""You are an academic research assistant for students with visual impairments. Please provide a comprehensive explanation about: {query}
                    Include:
                    1. A clear definition or explanation
                    2. Key concepts and theories
                    3. Important researchers or contributors in this field
                    4. Real-world applications or examples
                    5. Recent developments or current research trends

                    Keep the response educational, accessible, and well-structured for audio output."""

                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful academic research assistant for students with visual impairments."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500,
                        temperature=0.7
                    )

                    result = response.choices[0].message.content
                    
                    # Add to offline knowledge base
                    if self.offline_data_manager:
                        try:
                            self.offline_data_manager.add_to_knowledge_base(
                                category="AI_Generated",
                                question=query,
                                answer=result,
                                source="OpenAI GPT-4",
                                confidence=0.90,
                                difficulty_level="university",
                                academic_field="General"
                            )
                        except Exception as cache_error:
                            print(f"Could not cache to knowledge base: {cache_error}")

                    # Display detailed response in chat
                    detailed_response = f"""🤖 OpenAI Academic Assistant: "{query}"

{result}

💡 Source: OpenAI GPT-4 (Cached to Knowledge Base)"""

                    self.root.after(0, lambda: self.add_message("AIVI", detailed_response, "assistant"))

                    # Speak the response
                    safe_tts_speak(f"Academic information about {query}. {result[:300]}")

                    return result

                except Exception as e:
                    error_msg = f"OpenAI API error: {str(e)}. Please check your API key and internet connection."
                    print(error_msg)
                    return error_msg
            else:
                return "OpenAI is not installed. Please run: pip install openai"

        except Exception as e:
            error_msg = f"Academic search error: {str(e)}"
            return error_msg
    
    # Google Scholar removed - using OpenAI API with offline caching instead
    
    def search_enhanced(self, query):
        """Enhanced search with offline-first approach and multiple search modes"""
        try:
            if not self.offline_data:
                # Fall back to original search if enhanced components not available
                return self.search_academic(query)
            
            # Process search based on current mode
            if self.search_mode == "offline_first":
                # Try offline first, then online if needed
                result = self.offline_data.search_knowledge(query)
                if result and len(result.get('results', [])) > 0:
                    # Found good offline results
                    offline_response = self._format_offline_results(query, result)
                    self._add_to_knowledge_base(query, offline_response)
                    return offline_response
                else:
                    # No good offline results, try Google search
                    if self.google_search_manager:
                        google_result = self.google_search_manager.search(query)
                        if google_result.get('success'):
                            self._add_to_knowledge_base(query, google_result.get('summary', ''))
                            return self._format_google_results(query, google_result)
                    
                    # Fall back to AI if available
                    return self.search_academic(query)
                    
            elif self.search_mode == "google_first":
                # Try Google first, then offline
                if self.google_search_manager:
                    google_result = self.google_search_manager.search(query)
                    if google_result.get('success'):
                        self._add_to_knowledge_base(query, google_result.get('summary', ''))
                        return self._format_google_results(query, google_result)
                
                # Fall back to offline
                result = self.offline_data.search_knowledge(query)
                if result and len(result.get('results', [])) > 0:
                    return self._format_offline_results(query, result)
                
                # Final fallback to AI
                return self.search_academic(query)
                
            elif self.search_mode == "ai_only":
                # Use AI only
                return self.search_academic(query)
                
        except Exception as e:
            print(f"Enhanced search error: {e}")
            # Fall back to original search
            return self.search_academic(query)
    
    def _format_offline_results(self, query, result):
        """Format offline search results for display"""
        results = result.get('results', [])
        if not results:
            return f"No offline results found for '{query}'"
        
        formatted_response = f"📚 Offline Knowledge Base Results for: \"{query}\"\n\n"
        
        for i, res in enumerate(results[:3], 1):  # Show top 3 results
            formatted_response += f"📄 Result {i}:\n"
            formatted_response += f"Topic: {res.get('topic', 'Unknown')}\n"
            formatted_response += f"Content: {res.get('content', 'No content')[:300]}...\n"
            if res.get('source'):
                formatted_response += f"Source: {res.get('source')}\n"
            formatted_response += "\n"
        
        formatted_response += "🔍 Source: Local Knowledge Base"
        return formatted_response
    
    def _format_google_results(self, query, result):
        """Format Google search results for display"""
        summary = result.get('summary', 'No summary available')
        sources = result.get('sources', [])
        
        formatted_response = f"🌐 Google Search Results for: \"{query}\"\n\n"
        formatted_response += f"📝 Summary:\n{summary}\n\n"
        
        if sources:
            formatted_response += "📚 Sources:\n"
            for i, source in enumerate(sources[:3], 1):
                formatted_response += f"{i}. {source.get('title', 'No title')} - {source.get('url', 'No URL')}\n"
        
        formatted_response += "\n🔍 Source: Google Search (Cached)"
        return formatted_response
    
    def _add_to_knowledge_base(self, query, response):
        """Add search results to the knowledge base for future offline use"""
        try:
            if self.offline_data:
                self.offline_data.add_knowledge(
                    topic=query,
                    content=response,
                    source="search_cache",
                    metadata={
                        "search_mode": self.search_mode,
                        "timestamp": datetime.now().isoformat()
                    }
                )
        except Exception as e:
            print(f"Error adding to knowledge base: {e}")
    
    # Event handlers for tool cards
    def open_qa_tutor(self):
        """Open Q&A tutor dialog"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Q&A Tutor activated! Ask me any question about any subject."
        self.add_message("AIVI", message, "assistant")
        # Speak the activation
        safe_tts_speak(message)
    
    def open_deepseek_chat(self):
        """Open DeepSeek AI chat interface"""
        self.notebook.select(0)  # Switch to chat tab
        message = "🤖 DeepSeek AI activated! I'm ready to help with:\n• Academic questions and research\n• Programming and coding help\n• General knowledge and explanations\n• Creative writing assistance\n\nJust start your message with 'DeepSeek' or 'AI help' followed by your question."
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("DeepSeek AI is ready to assist you!")
    
    def open_math_solver(self):
        """Open enhanced math solver dialog with scrollable interface"""
        # Create a new window for the math solver
        math_window = tk.Toplevel(self.root)
        math_window.title("AIVI Math Solver")
        math_window.geometry("800x700")
        math_window.configure(bg=self.colors['bg'])
        math_window.resizable(True, True)
        
        # Make it modal
        math_window.transient(self.root)
        math_window.grab_set()
        
        # Center the window
        math_window.update_idletasks()
        x = (math_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (math_window.winfo_screenheight() // 2) - (700 // 2)
        math_window.geometry(f"800x700+{x}+{y}")
        
        # Main container
        main_frame = tk.Frame(math_window, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(header_frame,
                              text="🧮 AIVI Math Solver",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg'])
        title_label.pack(side='left')
        
        # Mode indicator
        mode_text = "📱 Offline Mode" if self.is_offline_mode else "🌐 Online Mode"
        mode_color = self.colors['warning'] if self.is_offline_mode else self.colors['success']
        mode_label = tk.Label(header_frame,
                             text=mode_text,
                             font=('Segoe UI', 12, 'bold'),
                             fg=mode_color,
                             bg=self.colors['bg'])
        mode_label.pack(side='right', pady=(10, 0))
        
        # Input section
        input_section = tk.Frame(main_frame, bg=self.colors['card_bg'], relief='solid', bd=1)
        input_section.pack(fill='x', pady=(0, 20))
        
        input_title = tk.Label(input_section,
                              text="Enter Math Problem:",
                              font=('Segoe UI', 14, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'])
        input_title.pack(pady=(15, 5))
        
        # Math input with better formatting
        input_frame = tk.Frame(input_section, bg=self.colors['card_bg'])
        input_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        math_input = tk.Text(input_frame,
                            font=('Segoe UI', 14),
                            bg=self.colors['input_bg'],
                            fg=self.colors['text'],
                            insertbackground=self.colors['accent'],
                            relief='solid',
                            bd=2,
                            height=3,
                            wrap='word')
        math_input.pack(fill='x', pady=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(input_section, bg=self.colors['card_bg'])
        buttons_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        solve_btn = tk.Button(buttons_frame,
                             text="🔍 Solve Problem",
                             command=lambda: self.solve_math_in_dialog(math_input, result_display, math_window),
                             bg=self.colors['accent'],
                             fg=self.colors['button_text'],
                             font=('Segoe UI', 12, 'bold'),
                             relief='solid',
                             bd=2,
                             padx=20,
                             pady=10,
                             cursor='hand2')
        solve_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(buttons_frame,
                             text="🗑️ Clear",
                             command=lambda: self.clear_math_dialog(math_input, result_display),
                             bg=self.colors['warning'],
                             fg=self.colors['button_text'],
                             font=('Segoe UI', 12, 'bold'),
                             relief='solid',
                             bd=2,
                             padx=20,
                             pady=10,
                             cursor='hand2')
        clear_btn.pack(side='left', padx=(0, 10))
        
        examples_btn = tk.Button(buttons_frame,
                                text="📚 Examples",
                                command=lambda: self.show_math_examples(math_input),
                                bg=self.colors['success'],
                                fg=self.colors['button_text'],
                                font=('Segoe UI', 12, 'bold'),
                                relief='solid',
                                bd=2,
                                padx=20,
                                pady=10,
                                cursor='hand2')
        examples_btn.pack(side='left')
        
        # Results section with scrolling
        results_section = tk.Frame(main_frame, bg=self.colors['card_bg'], relief='solid', bd=1)
        results_section.pack(fill='both', expand=True)
        
        results_title = tk.Label(results_section,
                                text="Results & History:",
                                font=('Segoe UI', 14, 'bold'),
                                fg=self.colors['text'],
                                bg=self.colors['card_bg'])
        results_title.pack(pady=(15, 5))
        
        # Scrollable results display
        results_frame = tk.Frame(results_section, bg=self.colors['card_bg'])
        results_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        result_display = scrolledtext.ScrolledText(results_frame,
                                                  font=('Segoe UI', 12),
                                                  bg=self.colors['input_bg'],
                                                  fg=self.colors['text'],
                                                  relief='solid',
                                                  bd=2,
                                                  wrap='word')
        result_display.pack(fill='both', expand=True)
        
        # Add welcome message
        welcome_msg = """🧮 Welcome to AIVI Math Solver!

I can help you solve various math problems:

Basic Arithmetic: 2 + 3 * 4, square root of 16
Algebra: solve x + 5 = 10, factor x^2 + 5x + 6  
Trigonometry: sin(30 degrees), cos(pi/4)
Calculus: derivative of x^2 + 3x + 1 (online mode)

Type your math problem above and click 'Solve Problem'!
"""
        result_display.insert(tk.END, welcome_msg)
        result_display.see(tk.END)
        
        # Bind Enter key to solve
        math_input.bind('<Control-Return>', lambda e: self.solve_math_in_dialog(math_input, result_display, math_window))
        
        # Focus on input
        math_input.focus_set()
        
        # Speak activation
        safe_tts_speak("Math solver opened. Enter your math problem and press Ctrl+Enter or click Solve Problem.")
    
    def solve_math_in_dialog(self, input_widget, result_widget, window):
        """Solve math problem in the dialog"""
        problem = input_widget.get("1.0", tk.END).strip()
        if not problem:
            safe_tts_speak("Please enter a math problem first.")
            return
        
        # Add problem to results
        timestamp = datetime.now().strftime("%H:%M:%S")
        result_widget.insert(tk.END, f"\n[{timestamp}] Problem: {problem}\n")
        result_widget.see(tk.END)
        result_widget.update()
        
        # Show solving message
        result_widget.insert(tk.END, "🔄 Solving...\n")
        result_widget.see(tk.END)
        result_widget.update()
        
        # Solve in separate thread
        def solve_async():
            try:
                import ai_assistant.math_reader as math_reader
                solution = math_reader.solve_math_problem(problem, gui_callback=True)
                
                # Update result display
                window.after(0, lambda: self.update_math_result(result_widget, solution, problem))
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                window.after(0, lambda: self.update_math_result(result_widget, error_msg, problem))
        
        threading.Thread(target=solve_async, daemon=True).start()
    
    def update_math_result(self, result_widget, solution, problem):
        """Update the math result display"""
        # Remove the "Solving..." message
        content = result_widget.get("1.0", tk.END)
        if "🔄 Solving...\n" in content:
            lines = content.split('\n')
            lines = [line for line in lines if "🔄 Solving..." not in line]
            result_widget.delete("1.0", tk.END)
            result_widget.insert("1.0", '\n'.join(lines))
        
        # Add solution
        result_widget.insert(tk.END, f"✅ {solution}\n")
        result_widget.insert(tk.END, "-" * 50 + "\n")
        result_widget.see(tk.END)
        
        # Speak result
        if "Solution:" in solution:
            safe_tts_speak(f"The answer is: {solution.replace('Solution:', '')}")
        else:
            safe_tts_speak(solution)
    
    def clear_math_dialog(self, input_widget, result_widget):
        """Clear the math dialog"""
        input_widget.delete("1.0", tk.END)
        result_widget.delete("1.0", tk.END)
        
        welcome_msg = """🧮 Math Solver Cleared!

Ready for new calculations. Enter your math problem above.
"""
        result_widget.insert(tk.END, welcome_msg)
        input_widget.focus_set()
        safe_tts_speak("Math solver cleared and ready for new problems.")
    
    def show_math_examples(self, input_widget):
        """Show math examples in the input"""
        import ai_assistant.math_reader as math_reader
        examples = math_reader.get_math_examples()
        
        # Create examples window
        examples_window = tk.Toplevel(self.root)
        examples_window.title("Math Examples")
        examples_window.geometry("600x500")
        examples_window.configure(bg=self.colors['bg'])
        
        # Center the window
        examples_window.update_idletasks()
        x = (examples_window.winfo_screenwidth() // 2) - (300)
        y = (examples_window.winfo_screenheight() // 2) - (250)
        examples_window.geometry(f"600x500+{x}+{y}")
        
        main_frame = tk.Frame(examples_window, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame,
                              text="📚 Math Examples",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg'])
        title_label.pack(pady=(0, 20))
        
        # Scrollable examples
        canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add example sections
        for category, example_list in examples.items():
            # Category header
            cat_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='solid', bd=1)
            cat_frame.pack(fill='x', pady=(0, 15))
            
            cat_label = tk.Label(cat_frame,
                               text=category,
                               font=('Segoe UI', 14, 'bold'),
                               fg=self.colors['accent'],
                               bg=self.colors['card_bg'])
            cat_label.pack(pady=10)
            
            # Example buttons
            for example in example_list:
                btn = tk.Button(cat_frame,
                               text=f"📝 {example}",
                               command=lambda ex=example: self.use_math_example(ex, input_widget, examples_window),
                               bg=self.colors['success'],
                               fg=self.colors['button_text'],
                               font=('Segoe UI', 10),
                               relief='solid',
                               bd=1,
                               padx=10,
                               pady=5,
                               cursor='hand2',
                               anchor='w')
                btn.pack(fill='x', padx=10, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        safe_tts_speak("Math examples window opened. Click on any example to use it.")
    
    def use_math_example(self, example, input_widget, examples_window):
        """Use a math example in the input"""
        input_widget.delete("1.0", tk.END)
        input_widget.insert("1.0", example)
        examples_window.destroy()
        input_widget.focus_set()
        safe_tts_speak(f"Example loaded: {example}")
    
    def open_note_taking(self):
        """Open note taking interface"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Note Taking activated! You can:\n• Say 'record lecture' to start recording\n• Type notes directly in the chat\n• Say 'summarize notes' to get a summary"
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Note taking activated. You can record lectures, type notes, or ask me to summarize content.")
    
    def open_content_search(self):
        """Open content search"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Content Search activated! Tell me what you'd like to search for. I can search using OpenAI's intelligent assistant or our comprehensive offline knowledge base with 512 university-level entries."
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Content search activated. What would you like me to search for?")
    
    def open_ocr_tool(self):
        """Open OCR text reading tool"""
        try:
            image_path = filedialog.askopenfilename(
                title="Select Image for OCR - AIVI will read the text aloud",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]
            )
            if image_path:
                self.notebook.select(0)  # Switch to chat tab
                message = f"Reading text from image: {image_path}"
                self.add_message("AIVI", message, "assistant")
                safe_tts_speak("Processing image. Please wait while I read the text.")
                
                # Process OCR in a separate thread
                def process_ocr():
                    try:
                        import ai_assistant.ocr as ocr
                        extracted_text = ocr.extract_text_from_image(image_path)
                        if extracted_text:
                            # Add OCR result to chat
                            self.root.after(0, lambda: self.add_message("AIVI", f"Text found in image:\n\n{extracted_text}", "assistant"))
                            safe_tts_speak(f"I found the following text: {extracted_text}")
                        else:
                            self.root.after(0, lambda: self.add_message("AIVI", "No text was found in the image.", "assistant"))
                            safe_tts_speak("I couldn't find any text in this image.")
                    except Exception as e:
                        error_msg = f"OCR error: {str(e)}"
                        self.root.after(0, lambda: self.add_message("AIVI", error_msg, "assistant"))
                        safe_tts_speak(f"There was an error reading the image: {str(e)}")
                
                threading.Thread(target=process_ocr, daemon=True).start()
        except Exception as e:
            self.add_message("AIVI", f"Error opening OCR tool: {str(e)}", "assistant")
    
    def open_braille_tool(self):
        """Open Braille conversion tool"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Braille Converter activated! You can:\n• Type text to convert to Braille\n• Say 'convert [text] to braille'\n• Say 'convert [braille] to text'"
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Braille converter activated. Tell me what text you'd like to convert to Braille, or give me Braille to convert to text.")
    
    def open_multimodal(self):
        """Open multi-modal input"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Multi-Modal Input activated! You can now use voice, text, images, and other input methods together. Try combining different types of input for enhanced interaction."
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Multi-modal input activated. You can now use voice, text, and images together.")
    
    def open_academic_search(self):
        """Open academic search with OpenAI and offline knowledge base"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Academic Search activated! I can help you research topics using OpenAI's intelligent assistant and our offline knowledge base with 512 university-level entries. Tell me what topic you'd like me to research, and I'll provide comprehensive academic information."
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Academic search activated. What topic would you like me to research using OpenAI and our knowledge base?")
    
    def start_quiz_mode(self):
        """Start quiz mode"""
        self.notebook.select(1)  # Switch to academic tab
        message = "Quiz Mode activated! I'll ask you questions to test your knowledge. Ready to start?"
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Quiz mode activated. I'll ask you questions to test your knowledge. Are you ready to start?")
    
    def open_academic_counsel(self):
        """Open academic counseling"""
        self.notebook.select(0)  # Switch to chat tab
        message = "Academic Counseling activated! I'm here to help with:\n• Study planning and organization\n• Academic goal setting\n• Learning strategies\n• Time management\n• Motivation and support\n\nWhat academic challenge would you like help with?"
        self.add_message("AIVI", message, "assistant")
        safe_tts_speak("Academic counseling activated. I'm here to help with your studies. What academic challenge would you like help with?")

    def open_pdf_reader(self):
        """Open PDF reader and extraction tool"""
        # Speak the action
        safe_tts_speak("Opening PDF reader. You can upload and read PDF documents.", self)

        # Create PDF reader dialog
        pdf_dialog = tk.Toplevel(self.root)
        pdf_dialog.title("PDF Reader & Extractor")
        pdf_dialog.geometry("700x600")
        pdf_dialog.configure(bg=self.colors['bg'])
        pdf_dialog.resizable(True, True)

        # Make dialog modal
        pdf_dialog.transient(self.root)
        pdf_dialog.grab_set()

        # Center the dialog
        pdf_dialog.update_idletasks()
        x = (pdf_dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (pdf_dialog.winfo_screenheight() // 2) - (600 // 2)
        pdf_dialog.geometry(f"700x600+{x}+{y}")

        # Title
        title_label = tk.Label(pdf_dialog,
                              text="📄 PDF Reader & Extractor",
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=(20, 10))

        # Subtitle
        subtitle_label = tk.Label(pdf_dialog,
                                 text="Extract complete text content from PDF documents",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(pady=(0, 10))

        # Info label
        info_label = tk.Label(pdf_dialog,
                             text="📋 Extracts full content including text, tables, and page information",
                             font=('Segoe UI', 10, 'italic'),
                             fg=self.colors['accent'],
                             bg=self.colors['bg'])
        info_label.pack(pady=(0, 15))

        # Main content frame
        main_frame = tk.Frame(pdf_dialog, bg=self.colors['card_bg'], relief='solid', bd=2)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Upload section
        upload_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        upload_section.pack(fill='x', padx=20, pady=20)

        tk.Label(upload_section,
                text="📁 Upload PDF File",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        # File selection frame
        file_frame = tk.Frame(upload_section, bg=self.colors['card_bg'])
        file_frame.pack(fill='x', pady=10)

        # Selected file display
        self.pdf_file_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(file_frame,
                             textvariable=self.pdf_file_var,
                             font=('Segoe UI', 11),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['input_bg'],
                             relief='solid',
                             bd=1,
                             anchor='w',
                             padx=10,
                             pady=8)
        file_label.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # Browse button
        browse_btn = tk.Button(file_frame,
                              text="📂 Browse",
                              command=lambda: self.browse_pdf_file(pdf_dialog),
                              bg=self.colors['accent'],
                              fg=self.colors['button_text'],
                              font=('Segoe UI', 11, 'bold'),
                              border=0,
                              relief='flat',
                              padx=20,
                              pady=8,
                              cursor='hand2',
                              activebackground=self.colors['accent_hover'],
                              activeforeground=self.colors['button_text'])
        browse_btn.pack(side='right')

        # Extraction options
        options_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        options_section.pack(fill='x', padx=20, pady=10)

        tk.Label(options_section,
                text="⚙️ Reading Options",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        # Reading options frame
        options_frame = tk.Frame(options_section, bg=self.colors['card_bg'])
        options_frame.pack(fill='x')

        self.read_aloud_var = tk.BooleanVar(value=True)
        read_cb = tk.Checkbutton(options_frame,
                                text="📢 Read extracted text aloud",
                                variable=self.read_aloud_var,
                                font=('Segoe UI', 11),
                                fg=self.colors['text'],
                                bg=self.colors['card_bg'],
                                selectcolor=self.colors['accent'],
                                activebackground=self.colors['card_bg'],
                                activeforeground=self.colors['text'])
        read_cb.pack(anchor='w', pady=2)

        self.save_text_var = tk.BooleanVar(value=False)
        save_cb = tk.Checkbutton(options_frame,
                                text="💾 Save extracted text to file",
                                variable=self.save_text_var,
                                font=('Segoe UI', 11),
                                fg=self.colors['text'],
                                bg=self.colors['card_bg'],
                                selectcolor=self.colors['accent'],
                                activebackground=self.colors['card_bg'],
                                activeforeground=self.colors['text'])
        save_cb.pack(anchor='w', pady=2)

        # Text display area
        text_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        text_section.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(text_section,
                text="📝 Extracted Text",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        # Text display with scrollbar
        text_frame = tk.Frame(text_section, bg=self.colors['card_bg'])
        text_frame.pack(fill='both', expand=True)

        self.pdf_text_display = scrolledtext.ScrolledText(text_frame,
                                                         height=15,
                                                         bg=self.colors['input_bg'],
                                                         fg=self.colors['text'],
                                                         font=('Segoe UI', 10),
                                                         border=2,
                                                         relief='solid',
                                                         highlightbackground=self.colors['border'],
                                                         highlightcolor=self.colors['accent'],
                                                         highlightthickness=2,
                                                         wrap='word')
        self.pdf_text_display.pack(fill='both', expand=True)

        # Action buttons
        btn_frame = tk.Frame(main_frame, bg=self.colors['card_bg'])
        btn_frame.pack(fill='x', padx=20, pady=20)

        # Extract button
        extract_btn = tk.Button(btn_frame,
                               text="📄 Extract Full Content",
                               command=lambda: self.extract_pdf_text(pdf_dialog),
                               bg=self.colors['accent'],
                               fg=self.colors['button_text'],
                               font=('Segoe UI', 12, 'bold'),
                               border=0,
                               relief='flat',
                               padx=25,
                               pady=12,
                               cursor='hand2',
                               activebackground=self.colors['accent_hover'],
                               activeforeground=self.colors['button_text'])
        extract_btn.pack(side='left', padx=(0, 10))

        # Read aloud button
        read_btn = tk.Button(btn_frame,
                            text="🔊 Read Aloud",
                            command=self.read_pdf_text_aloud,
                            bg=self.colors['success'],
                            fg=self.colors['button_text'],
                            font=('Segoe UI', 12, 'bold'),
                            border=0,
                            relief='flat',
                            padx=25,
                            pady=12,
                            cursor='hand2',
                            activebackground=self.colors['success'],
                            activeforeground=self.colors['button_text'])
        read_btn.pack(side='left', padx=(10, 10))

        # Close button
        close_btn = tk.Button(btn_frame,
                             text="❌ Close",
                             command=pdf_dialog.destroy,
                             bg=self.colors['card_bg'],
                             fg=self.colors['text'],
                             font=('Segoe UI', 12, 'bold'),
                             border=2,
                             relief='solid',
                             padx=25,
                             pady=12,
                             cursor='hand2',
                             activebackground=self.colors['border'],
                             activeforeground=self.colors['text'])
        close_btn.pack(side='right')

        # Initialize
        self.current_pdf_path = None
        self.extracted_text = ""
    def add_study_event(self):
        """Add a study event"""
        event_text = self.event_entry.get().strip()
        if event_text:
            try:
                import ai_assistant.study_planner as study_planner
                result = study_planner.add_event(event_text)
                self.event_entry.delete(0, tk.END)
                
                # Show success message
                message = f"Event added successfully: {event_text}"
                self.notebook.select(0)  # Switch to chat tab
                self.add_message("AIVI", message, "assistant")
                safe_tts_speak(f"Study event added: {event_text}")
            except Exception as e:
                error_msg = f"Error adding event: {str(e)}"
                self.add_message("AIVI", error_msg, "assistant")
                safe_tts_speak(f"Error adding event: {str(e)}")
        else:
            message = "Please enter an event description."
            safe_tts_speak("Please enter an event description.")
    
    def set_study_reminder(self):
        """Set a study reminder"""
        reminder_text = self.reminder_entry.get().strip()
        if reminder_text:
            try:
                import ai_assistant.study_planner as study_planner
                result = study_planner.set_reminder(reminder_text)
                self.reminder_entry.delete(0, tk.END)
                
                # Show success message
                message = f"Reminder set successfully: {reminder_text}"
                self.notebook.select(0)  # Switch to chat tab
                self.add_message("AIVI", message, "assistant")
                safe_tts_speak(f"Study reminder set: {reminder_text}")
            except Exception as e:
                error_msg = f"Error setting reminder: {str(e)}"
                self.add_message("AIVI", error_msg, "assistant")
                safe_tts_speak(f"Error setting reminder: {str(e)}")
        else:
            message = "Please enter a reminder description."
            safe_tts_speak("Please enter a reminder description.")
    
    def toggle_voice_mode(self):
        """Toggle voice recognition on/off with enhanced features"""
        self.is_listening = not self.is_listening
        
        if self.is_listening:
            self.voice_btn.config(text="🔴 Stop Voice", bg=self.colors['error'])
            self.update_status("Voice mode ON - Listening for commands", "success")
            safe_tts_speak("Voice mode activated. I'm listening for your commands.")
            
            # Use enhanced voice manager if available
            if self.enhanced_voice_manager:
                self.start_enhanced_voice_recognition()
            else:
                self.start_standard_voice_recognition()
        else:
            self.voice_btn.config(text="🎤 Start Voice", bg=self.colors['accent'])
            self.update_status("Voice mode OFF", "info")
            safe_tts_speak("Voice mode deactivated.")
            
            # Stop enhanced voice manager if active
            if self.enhanced_voice_manager:
                self.enhanced_voice_manager.stop()

    def start_enhanced_voice_recognition(self):
        """Start enhanced voice recognition with beep feedback and timeout"""
        def enhanced_voice_thread():
            try:
                while self.is_listening:
                    # Use enhanced voice manager with beep feedback
                    command = self.enhanced_voice_manager.listen_for_command()
                    if command and self.is_listening:
                        # Process the voice command
                        self.root.after(0, lambda cmd=command: self.process_enhanced_voice_command(cmd))
                    elif not self.is_listening:
                        break
            except Exception as e:
                error_msg = f"Enhanced voice recognition error: {str(e)}"
                self.safe_after(0, self.update_status, error_msg, "error")
                safe_tts_speak(f"Voice recognition error: {str(e)}")
                # Turn off voice mode
                self.safe_after(0, self.toggle_voice_mode)
        
        threading.Thread(target=enhanced_voice_thread, daemon=True).start()

    def start_standard_voice_recognition(self):
        """Start standard voice recognition (fallback)"""
        def start_voice_recognition():
            try:
                if voice_commands is not None:
                    while self.is_listening:
                        command = voice_commands.listen_for_command()
                        if command and self.is_listening:
                            # Process the voice command
                            self.root.after(0, lambda cmd=command: self.process_voice_command(cmd))
                else:
                    error_msg = "Voice recognition is not available. Speech recognition module is not installed."
                    self.safe_after(0, self.update_status, error_msg, "error")
                    safe_tts_speak(error_msg)
                    # Turn off voice mode since it's not available
                    self.safe_after(0, self.toggle_voice_mode)
            except Exception as e:
                error_msg = f"Voice recognition error: {str(e)}"
                self.safe_after(0, self.update_status, error_msg, "error")
                safe_tts_speak(f"Voice recognition error: {str(e)}")
        
        threading.Thread(target=start_voice_recognition, daemon=True).start()

    def process_enhanced_voice_command(self, command):
        """Process voice command with enhanced offline-first approach"""
        if command:
            # Add the voice command to chat
            self.add_message("You (Voice)", command, "user")
            
            # Try to process with enhanced search first
            try:
                # Use enhanced search for better results
                response = self.search_enhanced(command)
                self.add_message("AIVI", response, "assistant")
                
                # Extract main content for speech (remove formatting)
                speak_text = response.replace("📚", "").replace("🌐", "").replace("📄", "").replace("📝", "")
                speak_text = speak_text.replace("🔍", "").replace("\n", " ").strip()
                if len(speak_text) > 200:
                    speak_text = speak_text[:200] + "... Full details are shown in the chat."
                safe_tts_speak(speak_text)
                
            except Exception as e:
                # Fall back to standard command processing
                threading.Thread(target=self.process_command, args=(command,), daemon=True).start()

    def process_voice_command(self, command):
        """Process a voice command"""
        if command:
            # Add the voice command to chat
            self.add_message("You (Voice)", command, "user")
            # Process the command using the existing process_command method
            threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
    
    def toggle_mode(self):
        """Toggle between online and offline mode"""
        try:
            if self.is_offline_mode:
                # Switch to online mode
                import ai_assistant.offline_mode as offline_mode
                offline_mode.disable_offline_mode()
                self.is_offline_mode = False
                self.mode_btn.config(text="🌐 Online", bg=self.colors['success'])
                message = "Switched to Online mode - Full web access enabled"
                safe_tts_speak("Switched to online mode. Full web access enabled.")
            else:
                # Switch to offline mode
                import ai_assistant.offline_mode as offline_mode
                offline_mode.enable_offline_mode()
                self.is_offline_mode = True
                self.mode_btn.config(text="📱 Offline", bg=self.colors['warning'])
                message = "Switched to Offline mode - Using local knowledge base"
                safe_tts_speak("Switched to offline mode. Using local knowledge base.")
            
            self.update_status(message, "info")
            self.notebook.select(0)  # Switch to chat tab
            self.add_message("AIVI", message, "assistant")
            
        except Exception as e:
            error_msg = f"Error switching modes: {str(e)}"
            self.update_status(error_msg, "error")
            safe_tts_speak(f"Error switching modes: {str(e)}")
    
    def apply_voice_settings(self):
        """Apply voice settings"""
        try:
            selected_voice = self.voice_var.get()
            import ai_assistant.tts as tts
            
            # Apply voice mode
            if selected_voice == "Male":
                tts.set_voice_mode("male")
            elif selected_voice == "Female":
                tts.set_voice_mode("female")
            elif selected_voice == "Custom":
                tts.set_voice_mode("custom")
            else:
                tts.set_voice_mode("default")
            
            message = f"Voice settings applied: {selected_voice} voice mode"
            self.update_status(message, "success")
            safe_tts_speak(f"Voice settings applied. Now using {selected_voice.lower()} voice mode.")
            
        except Exception as e:
            error_msg = f"Could not apply voice settings: {str(e)}"
            messagebox.showerror("Error", error_msg)
            # Speak the error
            safe_tts_speak(error_msg)
        """Open math solver dialog"""
        # Speak the action
        safe_tts_speak("Opening Math Solver dialog.")
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Math Solver")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        title_label = tk.Label(dialog,
                              text="🧮 Math Solver",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=20)
        
        # Problem input
        tk.Label(dialog, text="Enter your math problem:", 
                font=('Segoe UI', 12),
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(pady=(0, 10))
        
        problem_text = scrolledtext.ScrolledText(dialog,
                                               height=8,
                                               bg=self.colors['input_bg'],
                                               fg=self.colors['text'],
                                               font=('Segoe UI', 12, 'bold'),
                                               border=2,
                                               relief='solid',
                                               highlightbackground=self.colors['border'],
                                               highlightcolor=self.colors['accent'],
                                               highlightthickness=2)
        problem_text.pack(padx=20, pady=10, fill='x')
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(pady=20)
        
        def solve_problem():
            problem = problem_text.get(1.0, tk.END).strip()
            if problem:
                try:
                    solution = math_reader.solve_math_problem(problem)
                    messagebox.showinfo("Solution", solution)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not solve problem: {str(e)}")
        
        tk.Button(btn_frame,
                 text="Solve",
                 command=solve_problem,
                 bg=self.colors['accent'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 activebackground=self.colors['accent_hover'],
                 activeforeground=self.colors['button_text']).pack(side='left', padx=10)
        
        tk.Button(btn_frame,
                 text="Close",
                 command=dialog.destroy,
                 bg=self.colors['card_bg'],
                 fg=self.colors['text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 activebackground=self.colors['border'],
                 activeforeground=self.colors['text']).pack(side='left')
    
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Braille Converter")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        
        # Title
        title_label = tk.Label(dialog,
                              text="⠠ Braille Converter",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=20)
        
        # Input text
        tk.Label(dialog, text="Enter text:", 
                font=('Segoe UI', 12),
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(pady=(0, 5))
        
        input_text = scrolledtext.ScrolledText(dialog,
                                             height=6,
                                             bg=self.colors['input_bg'],
                                             fg=self.colors['text'],
                                             font=('Segoe UI', 12, 'bold'),
                                             border=2,
                                             relief='solid',
                                             highlightbackground=self.colors['border'],
                                             highlightcolor=self.colors['accent'],
                                             highlightthickness=2)
        input_text.pack(padx=20, pady=5, fill='x')
        
        # Output text
        tk.Label(dialog, text="Result:", 
                font=('Segoe UI', 12),
                fg=self.colors['text'], 
                bg=self.colors['bg']).pack(pady=(10, 5))
        
        output_text = scrolledtext.ScrolledText(dialog,
                                              height=6,
                                              bg=self.colors['input_bg'],
                                              fg=self.colors['text'],
                                              font=('Segoe UI', 12, 'bold'),
                                              border=2,
                                              relief='solid',
                                              highlightbackground=self.colors['border'],
                                              highlightcolor=self.colors['accent'],
                                              highlightthickness=2)
        output_text.pack(padx=20, pady=5, fill='x')
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(pady=20)
        
        def text_to_braille():
            text = input_text.get(1.0, tk.END).strip()
            if text:
                try:
                    braille_result = braille.text_to_braille(text)
                    output_text.delete(1.0, tk.END)
                    output_text.insert(1.0, braille_result)
                except Exception as e:
                    messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        
        def braille_to_text():
            braille_input = input_text.get(1.0, tk.END).strip()
            if braille_input:
                try:
                    text_result = braille.braille_to_text(braille_input)
                    output_text.delete(1.0, tk.END)
                    output_text.insert(1.0, text_result)
                except Exception as e:
                    messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        
        tk.Button(btn_frame,
                 text="Text → Braille",
                 command=text_to_braille,
                 bg=self.colors['accent'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=20,
                 pady=10,
                 activebackground=self.colors['accent_hover'],
                 activeforeground=self.colors['button_text']).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="Braille → Text",
                 command=braille_to_text,
                 bg=self.colors['success'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=20,
                 pady=10,
                 activebackground=self.colors['success'],
                 activeforeground=self.colors['button_text']).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="Close",
                 command=dialog.destroy,
                 bg=self.colors['card_bg'],
                 fg=self.colors['text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=20,
                 pady=10,
                 activebackground=self.colors['border'],
                 activeforeground=self.colors['text']).pack(side='left', padx=5)
    
    def open_web_search(self):
        """Open web search"""
        # Speak the action
        safe_tts_speak("Opening web search options.")
        
        choice = messagebox.askyesnocancel("Web Search", "Choose search engine:\nYes = Google\nNo = YouTube\nCancel = Back")
        if choice is True:
            os.system("start https://www.google.com")
            self.update_status("Opened Google in browser", "success")
            # Speak the action
            safe_tts_speak("Opened Google in your browser.")
        elif choice is False:
            os.system("start https://www.youtube.com")
            self.update_status("Opened YouTube in browser", "success")
            # Speak the action
            safe_tts_speak("Opened YouTube in your browser.")
    
    def open_offline_voice_control(self):
        """Open offline voice control interface"""
        if offline_voice is None:
            messagebox.showerror("Not Available",
                               "Offline voice control is not available.\n\n" +
                               "Please install required libraries:\n" +
                               "pip install SpeechRecognition pocketsphinx pyaudio")
            safe_tts_speak("Offline voice control is not available. Please install required libraries.", self)
            return

        # Create offline voice control dialog
        voice_dialog = tk.Toplevel(self.root)
        voice_dialog.title("Offline Voice Control")
        voice_dialog.geometry("600x500")
        voice_dialog.configure(bg=self.colors['bg'])
        voice_dialog.resizable(True, True)

        # Make dialog modal
        voice_dialog.transient(self.root)
        voice_dialog.grab_set()

        # Center the dialog
        voice_dialog.update_idletasks()
        x = (voice_dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (voice_dialog.winfo_screenheight() // 2) - (500 // 2)
        voice_dialog.geometry(f"600x500+{x}+{y}")

        # Title
        title_label = tk.Label(voice_dialog,
                              text="🎤 Offline Voice Control",
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=(20, 10))

        # Status indicator
        self.voice_status = tk.Label(voice_dialog,
                                    text="🔴 Voice Control Stopped",
                                    font=('Segoe UI', 14, 'bold'),
                                    fg='red',
                                    bg=self.colors['bg'])
        self.voice_status.pack(pady=10)

        # Instructions
        instructions = tk.Label(voice_dialog,
                               text="Voice commands work without internet connection\n" +
                                    "Click 'Start Voice Control' and say commands clearly",
                               font=('Segoe UI', 12),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg'])
        instructions.pack(pady=(0, 20))

        # Control buttons frame
        controls_frame = tk.Frame(voice_dialog, bg=self.colors['bg'])
        controls_frame.pack(pady=20)

        # Start/Stop button
        self.voice_control_btn = tk.Button(controls_frame,
                                          text="🎤 Start Voice Control",
                                          command=lambda: self.toggle_offline_voice_control(voice_dialog),
                                          bg='#4CAF50',
                                          fg='white',
                                          font=('Segoe UI', 14, 'bold'),
                                          padx=30,
                                          pady=15)
        self.voice_control_btn.pack(side='left', padx=10)

        # Help button
        help_btn = tk.Button(controls_frame,
                            text="📋 Voice Commands",
                            command=self.show_voice_help,
                            bg=self.colors['accent'],
                            fg=self.colors['button_text'],
                            font=('Segoe UI', 12, 'bold'),
                            padx=20,
                            pady=15)
        help_btn.pack(side='left', padx=10)

        # Voice feedback area
        feedback_frame = tk.Frame(voice_dialog, bg=self.colors['card_bg'], relief='solid', bd=2)
        feedback_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(feedback_frame,
                text="🗣️ Voice Activity Log",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(pady=(10, 5))

        # Voice log display
        self.voice_log = scrolledtext.ScrolledText(feedback_frame,
                                                  bg=self.colors['input_bg'],
                                                  fg=self.colors['text'],
                                                  font=('Segoe UI', 11),
                                                  wrap='word',
                                                  height=12)
        self.voice_log.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Add initial message
        self.voice_log.insert(tk.END, "📋 Offline Voice Control Ready\n\n")
        self.voice_log.insert(tk.END, "Available commands:\n")
        self.voice_log.insert(tk.END, "• 'Open Calculator' - Launch calculator\n")
        self.voice_log.insert(tk.END, "• 'Open Notepad' - Launch notepad\n")
        self.voice_log.insert(tk.END, "• 'Take Screenshot' - Capture screen\n")
        self.voice_log.insert(tk.END, "• 'Help' - Show all commands\n")
        self.voice_log.insert(tk.END, "• 'Stop Listening' - End voice control\n\n")

        safe_tts_speak("Offline voice control interface opened. Click start voice control to begin.", self)

    def toggle_offline_voice_control(self, dialog):
        """Toggle offline voice control on/off"""
        if not self.offline_voice_active:
            # Start voice control
            if offline_voice.is_offline_voice_available():
                self.offline_voice_active = True
                self.voice_status.config(text="🟢 Voice Control Active", fg='green')
                self.voice_control_btn.config(text="🛑 Stop Voice Control", bg='#f44336')

                # Start listening with callback
                offline_voice.start_offline_voice_control(self.handle_offline_voice_command)

                self.voice_log.insert(tk.END, "🎤 Voice control started. Listening for commands...\n")
                self.voice_log.see(tk.END)

                safe_tts_speak("Voice control started. I'm listening for your commands.", self)
            else:
                messagebox.showerror("Error", "Voice recognition libraries not available.", parent=dialog)
        else:
            # Stop voice control
            self.offline_voice_active = False
            self.voice_status.config(text="🔴 Voice Control Stopped", fg='red')
            self.voice_control_btn.config(text="🎤 Start Voice Control", bg='#4CAF50')

            offline_voice.stop_offline_voice_control()

            self.voice_log.insert(tk.END, "🛑 Voice control stopped.\n")
            self.voice_log.see(tk.END)

            safe_tts_speak("Voice control stopped.", self)

    def handle_offline_voice_command(self, command, result):
        """Handle offline voice command results"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Log the command
        self.voice_log.insert(tk.END, f"[{timestamp}] Command: {command}\n")
        self.voice_log.insert(tk.END, f"[{timestamp}] Result: {result}\n\n")
        self.voice_log.see(tk.END)

        # Speak the result
        safe_tts_speak(result, self)

        # Update status if needed
        if command == 'stop_listening':
            self.offline_voice_active = False
            self.voice_status.config(text="🔴 Voice Control Stopped", fg='red')
            self.voice_control_btn.config(text="🎤 Start Voice Control", bg='#4CAF50')

    def show_voice_help(self):
        """Show offline voice commands help"""
        if offline_voice:
            help_text = offline_voice.get_offline_voice_help()
            messagebox.showinfo("Voice Commands", help_text)
            safe_tts_speak("Voice commands help displayed.", self)
        else:
            messagebox.showinfo("Help", "Offline voice control not available.")
    
    def open_academic_search_dialog(self):
        """Open academic search dialog with OpenAI and offline knowledge base"""
        # Speak the action
        safe_tts_speak("Opening academic research search.")

        dialog = tk.Toplevel(self.root)
        dialog.title("Academic Research Search")
        dialog.geometry("700x600")
        dialog.configure(bg=self.colors['bg'])

        # Title
        title_label = tk.Label(dialog,
                              text="📚 Academic Research Search",
                              font=('Segoe UI', 18, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=20)

        # Search input
        search_frame = tk.Frame(dialog, bg=self.colors['bg'])
        search_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(search_frame, text="Search Topic:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg']).pack(anchor='w')

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame,
                               textvariable=search_var,
                               font=('Segoe UI', 12, 'bold'),
                               bg=self.colors['input_bg'],
                               fg=self.colors['text'],
                               insertbackground=self.colors['accent'],
                               border=2,
                               relief='solid',
                               highlightbackground=self.colors['border'],
                               highlightcolor=self.colors['accent'],
                               highlightthickness=2)
        search_entry.pack(fill='x', pady=(5, 0), ipady=10)

        # Results display
        tk.Label(dialog, text="Search Results:",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg']).pack(anchor='w', padx=20, pady=(20, 5))

        results_text = scrolledtext.ScrolledText(dialog,
                                               height=15,
                                               bg=self.colors['input_bg'],
                                               fg=self.colors['text'],
                                               font=('Segoe UI', 11, 'bold'),
                                               border=2,
                                               relief='solid',
                                               highlightbackground=self.colors['border'],
                                               highlightcolor=self.colors['accent'],
                                               highlightthickness=2,
                                               wrap='word')
        results_text.pack(padx=20, pady=5, fill='both', expand=True)

        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.colors['bg'])
        btn_frame.pack(pady=20)

        def perform_search():
            query = search_var.get().strip()
            if query:
                results_text.delete(1.0, tk.END)
                results_text.insert(1.0, "Searching academic resources... Please wait.")
                dialog.update()

                # Perform search in thread to avoid blocking UI
                def search_thread():
                    try:
                        result = self.search_academic(query)
                        # Update UI in main thread
                        dialog.after(0, lambda: update_results(result))
                    except Exception as e:
                        error_msg = f"Search failed: {str(e)}"
                        dialog.after(0, lambda: update_results(error_msg))

                def update_results(result):
                    results_text.delete(1.0, tk.END)
                    results_text.insert(1.0, result)
                
                threading.Thread(target=search_thread, daemon=True).start()
        
        def speak_results():
            content = results_text.get(1.0, tk.END).strip()
            if content and content != "Searching academic resources... Please wait.":
                safe_tts_speak(content)
            else:
                safe_tts_speak("No results to read.")
        
        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: perform_search())
        
        tk.Button(btn_frame,
                 text="Search",
                 command=perform_search,
                 bg=self.colors['accent'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 activebackground=self.colors['accent_hover'],
                 activeforeground=self.colors['button_text']).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="🔊 Speak Results",
                 command=speak_results,
                 bg=self.colors['success'],
                 fg=self.colors['button_text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 activebackground=self.colors['success'],
                 activeforeground=self.colors['button_text']).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="Close",
                 command=dialog.destroy,
                 bg=self.colors['card_bg'],
                 fg=self.colors['text'],
                 font=('Segoe UI', 11, 'bold'),
                 border=2,
                 relief='solid',
                 padx=25,
                 pady=10,
                 activebackground=self.colors['border'],
                 activeforeground=self.colors['text']).pack(side='left', padx=5)
        
        # Focus on search entry
        search_entry.focus_set()
    
    def add_study_event(self):
        """Add a study event"""
        event = self.event_entry.get().strip()
        if event:
            try:
                study_planner.add_event(event)
                self.event_entry.delete(0, tk.END)
                self.update_status(f"Event added: {event}", "success")
                messagebox.showinfo("Success", "Event added successfully!")
                # Speak confirmation
                safe_tts_speak(f"Event added: {event}")
            except Exception as e:
                error_msg = f"Could not add event: {str(e)}"
                messagebox.showerror("Error", error_msg)
                # Speak error
                safe_tts_speak(error_msg)
    
    def set_study_reminder(self):
        """Set a study reminder"""
        reminder = self.reminder_entry.get().strip()
        if reminder:
            try:
                study_planner.set_reminder(reminder)
                self.reminder_entry.delete(0, tk.END)  
                self.update_status(f"Reminder set: {reminder}", "success")
                messagebox.showinfo("Success", "Reminder set successfully!")
                # Speak confirmation
                safe_tts_speak(f"Reminder set: {reminder}")
            except Exception as e:
                error_msg = f"Could not set reminder: {str(e)}"
                messagebox.showerror("Error", error_msg)
                # Speak error
                safe_tts_speak(error_msg)
    
    def toggle_mode(self):
        """Toggle between online and offline mode"""
        if not self.is_offline_mode:
            # Switch to offline
            offline_mode.enable_offline_mode()
            self.is_offline_mode = True
            self.mode_btn.config(text="📱 Offline", bg=self.colors['warning'],
                               activebackground=self.colors['warning'])
            offline_academic.set_mode('offline')
            self.update_status("Switched to offline mode", "warning")
            # Speak the mode change
            safe_tts_speak("Switched to offline mode.")
        else:
            # Switch to online
            offline_mode.disable_offline_mode()
            self.is_offline_mode = False
            self.mode_btn.config(text="🌐 Online", bg=self.colors['success'],
                               activebackground=self.colors['success'])
            offline_academic.set_mode('online')
            self.update_status("Switched to online mode", "success")
            # Speak the mode change
            safe_tts_speak("Switched to online mode.")
    
    def apply_voice_settings(self):
        """Apply voice settings"""
        voice_mode = self.voice_var.get().lower()
        try:
            if hasattr(tts, 'set_voice_mode'):
                result = tts.set_voice_mode(voice_mode)
                if result:
                    success_msg = f"Voice mode changed to {voice_mode}"
                    self.update_status(success_msg, "success")
                    messagebox.showinfo("Success", success_msg)
                    # Speak the confirmation
                    safe_tts_speak(success_msg)
                else:
                    error_msg = f"Could not change to {voice_mode} voice mode"
                    messagebox.showerror("Error", error_msg)
                    # Speak the error
                    safe_tts_speak(error_msg)
            else:
                warning_msg = "Voice mode switching is not supported in this configuration"
                messagebox.showwarning("Warning", warning_msg)
                # Speak the warning
                safe_tts_speak(warning_msg)
        except Exception as e:
            error_msg = f"Could not apply voice settings: {str(e)}"
            messagebox.showerror("Error", error_msg)
            # Speak the error
            safe_tts_speak(error_msg)
    
    def on_closing(self):
        """Handle application shutdown"""
        self.is_running = False
        
        # Cancel any pending timer jobs
        if self.timer_job:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
                
        if self.resize_job:
            try:
                self.root.after_cancel(self.resize_job)
            except tk.TclError:
                pass
        
        # Close the application
        try:
            self.root.destroy()
        except tk.TclError:
            pass
    
    def open_voice_settings(self):
        """Open voice and speech settings dialog"""
        # Speak the action
        safe_tts_speak("Opening voice settings.")

        # Create settings dialog
        settings_dialog = tk.Toplevel(self.root)
        settings_dialog.title("Voice & Speech Settings")
        settings_dialog.geometry("500x600")
        settings_dialog.configure(bg=self.colors['bg'])
        settings_dialog.resizable(False, False)

        # Make dialog modal
        settings_dialog.transient(self.root)
        settings_dialog.grab_set()

        # Center the dialog
        settings_dialog.update_idletasks()
        x = (settings_dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (settings_dialog.winfo_screenheight() // 2) - (600 // 2)
        settings_dialog.geometry(f"500x600+{x}+{y}")

        # Title
        title_label = tk.Label(settings_dialog,
                              text="🔊 Voice & Speech Settings",
                              font=('Segoe UI', 20, 'bold'),
                              fg=self.colors['text'],
                              bg=self.colors['bg'])
        title_label.pack(pady=(20, 30))

        # Main settings frame
        main_frame = tk.Frame(settings_dialog, bg=self.colors['card_bg'], relief='solid', bd=2)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Load current settings
        current_voice = getattr(tts, 'get_voice_mode', lambda: 'default')()

        # Voice Gender Section
        voice_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        voice_section.pack(fill='x', padx=20, pady=20)

        tk.Label(voice_section,
                text="Voice Gender",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        self.voice_gender_var = tk.StringVar(value='default')
        if 'male' in str(current_voice).lower():
            self.voice_gender_var.set('male')
        elif 'female' in str(current_voice).lower():
            self.voice_gender_var.set('female')

        voice_options = [
            ('Default', 'default'),
            ('Male Voice', 'male'),
            ('Female Voice', 'female')
        ]

        for text, value in voice_options:
            rb = tk.Radiobutton(voice_section,
                               text=text,
                               variable=self.voice_gender_var,
                               value=value,
                               font=('Segoe UI', 12),
                               fg=self.colors['text'],
                               bg=self.colors['card_bg'],
                               selectcolor=self.colors['accent'],
                               activebackground=self.colors['card_bg'],
                               activeforeground=self.colors['text'],
                               command=lambda: self.preview_voice_setting())
            rb.pack(anchor='w', pady=5)

        # Speed Section
        speed_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        speed_section.pack(fill='x', padx=20, pady=20)

        tk.Label(speed_section,
                text="Speech Speed",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        speed_frame = tk.Frame(speed_section, bg=self.colors['card_bg'])
        speed_frame.pack(fill='x')

        tk.Label(speed_frame,
                text="Slow",
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']).pack(side='left')

        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = tk.Scale(speed_frame,
                                   from_=0.5,
                                   to=2.0,
                                   resolution=0.1,
                                   orient='horizontal',
                                   variable=self.speed_var,
                                   bg=self.colors['card_bg'],
                                   fg=self.colors['text'],
                                   highlightbackground=self.colors['card_bg'],
                                   activebackground=self.colors['accent'],
                                   troughcolor=self.colors['input_bg'],
                                   command=lambda x: self.preview_voice_setting())
        self.speed_scale.pack(side='left', fill='x', expand=True, padx=10)

        tk.Label(speed_frame,
                text="Fast",
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']).pack(side='right')

        # Volume Section
        volume_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        volume_section.pack(fill='x', padx=20, pady=20)

        tk.Label(volume_section,
                text="Speech Volume",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        volume_frame = tk.Frame(volume_section, bg=self.colors['card_bg'])
        volume_frame.pack(fill='x')

        tk.Label(volume_frame,
                text="Quiet",
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']).pack(side='left')

        self.volume_var = tk.DoubleVar(value=1.0)
        self.volume_scale = tk.Scale(volume_frame,
                                    from_=0.1,
                                    to=1.0,
                                    resolution=0.1,
                                    orient='horizontal',
                                    variable=self.volume_var,
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['text'],
                                    highlightbackground=self.colors['card_bg'],
                                    activebackground=self.colors['accent'],
                                    troughcolor=self.colors['input_bg'],
                                    command=lambda x: self.preview_voice_setting())
        self.volume_scale.pack(side='left', fill='x', expand=True, padx=10)

        tk.Label(volume_frame,
                text="Loud",
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']).pack(side='right')

        # Test Speech Section
        test_section = tk.Frame(main_frame, bg=self.colors['card_bg'])
        test_section.pack(fill='x', padx=20, pady=20)

        tk.Label(test_section,
                text="Test Speech",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card_bg']).pack(anchor='w', pady=(0, 10))

        test_btn = tk.Button(test_section,
                            text="🎵 Test Voice",
                            command=self.test_voice_settings,
                            bg=self.colors['accent'],
                            fg=self.colors['button_text'],
                            font=('Segoe UI', 12, 'bold'),
                            border=0,
                            relief='flat',
                            padx=20,
                            pady=10,
                            cursor='hand2',
                            activebackground=self.colors['accent_hover'],
                            activeforeground=self.colors['button_text'])
        test_btn.pack(pady=10)

        # Buttons section
        btn_frame = tk.Frame(main_frame, bg=self.colors['card_bg'])
        btn_frame.pack(fill='x', side='bottom', padx=20, pady=20)

        def save_settings():
            self.save_voice_settings()
            settings_dialog.destroy()
            safe_tts_speak("Voice settings saved successfully.")

        def cancel_settings():
            settings_dialog.destroy()
            safe_tts_speak("Settings cancelled.")

        save_btn = tk.Button(btn_frame,
                            text="💾 Save Settings",
                            command=save_settings,
                            bg=self.colors['success'],
                            fg=self.colors['button_text'],
                            font=('Segoe UI', 12, 'bold'),
                            border=0,
                            relief='flat',
                            padx=30,
                            pady=12,
                            cursor='hand2',
                            activebackground=self.colors['success'],
                            activeforeground=self.colors['button_text'])
        save_btn.pack(side='left', padx=(0, 10))

        cancel_btn = tk.Button(btn_frame,
                              text="❌ Cancel",
                              command=cancel_settings,
                              bg=self.colors['card_bg'],
                              fg=self.colors['text'],
                              font=('Segoe UI', 12, 'bold'),
                              border=2,
                              relief='solid',
                              padx=30,
                              pady=12,
                              cursor='hand2',
                              activebackground=self.colors['border'],
                              activeforeground=self.colors['text'])
        cancel_btn.pack(side='right', padx=(10, 0))

        # Load saved settings if they exist
        self.load_voice_settings()

    def preview_voice_setting(self):
        """Preview voice settings when changed"""
        try:
            voice = self.voice_gender_var.get()
            speed = self.speed_var.get()
            # Don't speak during preview to avoid overwhelming
            pass
        except Exception as e:
            print(f"Preview error: {e}")

    def test_voice_settings(self):
        """Test current voice settings"""
        try:
            voice = self.voice_gender_var.get()
            speed = self.speed_var.get()
            volume = self.volume_var.get()

            # Apply temporary settings and test
            import ai_assistant.tts as tts_module
            test_text = f"Hello! This is a test of your voice settings. Voice is set to {voice}, speed is {speed:.1f}, and volume is {volume:.1f}."
            tts_module.speak_text(test_text, voice=voice, speed=speed)

        except Exception as e:
            safe_tts_speak(f"Test failed: {str(e)}")

    def save_voice_settings(self):
        """Save voice settings to file and apply them"""
        try:
            settings = {
                'voice_gender': self.voice_gender_var.get(),
                'speech_speed': self.speed_var.get(),
                'speech_volume': self.volume_var.get()
            }

            # Save to JSON file
            import json
            with open('voice_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)

            # Apply settings to TTS
            import ai_assistant.tts as tts_module
            tts_module.set_voice_mode(settings['voice_gender'])

            # Store settings in class for later use
            self.voice_settings = settings

            print(f"Voice settings saved: {settings}")

        except Exception as e:
            print(f"Failed to save voice settings: {e}")
            safe_tts_speak(f"Failed to save settings: {str(e)}")

    def load_voice_settings(self):
        """Load voice settings from file"""
        try:
            import json
            import os

            if os.path.exists('voice_settings.json'):
                with open('voice_settings.json', 'r') as f:
                    settings = json.load(f)

                # Apply loaded settings to UI
                if hasattr(self, 'voice_gender_var'):
                    self.voice_gender_var.set(settings.get('voice_gender', 'default'))
                if hasattr(self, 'speed_var'):
                    self.speed_var.set(settings.get('speech_speed', 1.0))
                if hasattr(self, 'volume_var'):
                    self.volume_var.set(settings.get('speech_volume', 1.0))

                # Store in class
                self.voice_settings = settings

                print(f"Voice settings loaded: {settings}")

        except Exception as e:
            print(f"Failed to load voice settings: {e}")
            # Set default settings
            self.voice_settings = {
                'voice_gender': 'default',
                'speech_speed': 1.0,
                'speech_volume': 1.0
            }

    def browse_pdf_file(self, dialog):
        """Browse and select a PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            parent=dialog
        )

        if file_path:
            self.current_pdf_path = file_path
            filename = os.path.basename(file_path)
            self.pdf_file_var.set(f"Selected: {filename}")
            safe_tts_speak(f"Selected PDF file: {filename}", self)

    def extract_pdf_text(self, dialog):
        """Extract text from the selected PDF"""
        if not self.current_pdf_path:
            messagebox.showwarning("No File", "Please select a PDF file first.", parent=dialog)
            safe_tts_speak("Please select a PDF file first.", self)
            return

        try:
            safe_tts_speak("Extracting text from PDF. Please wait.", self)

            # Try to extract using PyPDF2 first, then pdfplumber as fallback
            extracted_text = self.extract_text_from_pdf(self.current_pdf_path)

            if extracted_text.strip():
                self.extracted_text = extracted_text
                self.pdf_text_display.delete(1.0, tk.END)
                self.pdf_text_display.insert(1.0, extracted_text)

                # Count pages and words
                word_count = len(extracted_text.split())
                safe_tts_speak(f"Text extracted successfully. Found {word_count} words.", self)

                # Auto-read if option is enabled
                if self.read_aloud_var.get():
                    self.read_pdf_text_aloud()

                # Auto-save if option is enabled
                if self.save_text_var.get():
                    self.save_extracted_text()

            else:
                self.pdf_text_display.delete(1.0, tk.END)
                self.pdf_text_display.insert(1.0, "No text could be extracted from this PDF. The PDF might contain only images or be password protected.")
                safe_tts_speak("No text could be extracted from this PDF. It might contain only images.", self)

        except Exception as e:
            error_msg = f"Failed to extract text: {str(e)}"
            messagebox.showerror("Extraction Error", error_msg, parent=dialog)
            safe_tts_speak(f"Extraction failed: {str(e)}", self)

    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from PDF using available libraries with enhanced extraction"""
        extracted_text = ""
        total_pages = 0

        # Try pdfplumber first (better for complex layouts)
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                print(f"Processing PDF with {total_pages} pages...")

                for page_num, page in enumerate(pdf.pages):
                    print(f"Extracting text from page {page_num + 1}...")

                    # Extract text with better formatting
                    text = page.extract_text()

                    # Also try to extract tables if any
                    tables = page.extract_tables()

                    if text and text.strip():
                        # Clean and format the text
                        cleaned_text = self.clean_extracted_text(text)
                        extracted_text += f"\n=== PAGE {page_num + 1} ===\n{cleaned_text}\n"

                    # Add table content if found
                    if tables:
                        for table_num, table in enumerate(tables):
                            extracted_text += f"\n--- Table {table_num + 1} on Page {page_num + 1} ---\n"
                            for row in table:
                                if row:
                                    # Filter out None values and join
                                    row_text = " | ".join([str(cell) if cell is not None else "" for cell in row])
                                    if row_text.strip():
                                        extracted_text += f"{row_text}\n"
                            extracted_text += "\n"

            if extracted_text.strip():
                return f"📄 PDF CONTENT EXTRACTED SUCCESSFULLY 📄\nTotal Pages: {total_pages}\n\n{extracted_text}"

        except ImportError:
            print("pdfplumber not available, trying PyPDF2...")
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")

        # Try PyPDF2 as fallback
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                print(f"Processing PDF with {total_pages} pages using PyPDF2...")

                for page_num, page in enumerate(pdf_reader.pages):
                    print(f"Extracting text from page {page_num + 1}...")
                    text = page.extract_text()
                    if text.strip():
                        cleaned_text = self.clean_extracted_text(text)
                        extracted_text += f"\n=== PAGE {page_num + 1} ===\n{cleaned_text}\n"

            if extracted_text.strip():
                return f"📄 PDF CONTENT EXTRACTED SUCCESSFULLY 📄\nTotal Pages: {total_pages}\n\n{extracted_text}"

        except ImportError:
            print("PyPDF2 not available")
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}")

        # If no text extracted, provide detailed feedback
        if not extracted_text.strip():
            extracted_text = f"""❌ NO TEXT CONTENT EXTRACTED ❌

Possible reasons:
• PDF contains only images/scanned documents (needs OCR)
• PDF is password protected
• PDF has complex formatting that requires specialized tools
• PDF libraries not installed

📋 TO IMPROVE PDF READING:
• Install libraries: pip install PyPDF2 pdfplumber
• For image PDFs: pip install pytesseract (OCR support)
• Try converting PDF to text format first

📄 FILE INFO:
• File: {os.path.basename(pdf_path)}
• Size: {os.path.getsize(pdf_path)} bytes"""

        return extracted_text

    def clean_extracted_text(self, text):
        """Clean and format extracted text for better readability"""
        if not text:
            return ""

        # Remove excessive whitespace
        import re

        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)

        # Replace multiple newlines with double newline
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        # Remove trailing/leading whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        # Remove excessive whitespace at beginning and end
        text = text.strip()

        return text

    def read_pdf_text_aloud(self):
        """Read the extracted PDF text aloud"""
        if not hasattr(self, 'extracted_text') or not self.extracted_text.strip():
            safe_tts_speak("No text available to read. Please extract text from a PDF first.", self)
            return

        try:
            # Clean up the text for better speech
            text_to_read = self.extracted_text

            # Remove page markers for smoother reading
            import re
            text_to_read = re.sub(r'\n---\s*Page\s*\d+\s*---\n', '\n\nNew page. ', text_to_read)

            # Clean up extra whitespace
            text_to_read = re.sub(r'\n\s*\n', '\n\n', text_to_read)
            text_to_read = text_to_read.strip()

            # Speak the text
            safe_tts_speak("Starting to read PDF content.", self)

            # For very long texts, read in chunks to avoid overwhelming
            max_chunk_size = 2000  # characters
            if len(text_to_read) > max_chunk_size:
                chunks = [text_to_read[i:i+max_chunk_size] for i in range(0, len(text_to_read), max_chunk_size)]
                for i, chunk in enumerate(chunks[:3]):  # Limit to first 3 chunks
                    safe_tts_speak(chunk, self)
                    if i < len(chunks) - 1:
                        safe_tts_speak("Continuing with next section.", self)

                if len(chunks) > 3:
                    safe_tts_speak(f"This PDF contains {len(chunks)} sections. Only the first 3 sections were read aloud. You can view the full text in the display area.", self)
            else:
                safe_tts_speak(text_to_read, self)

        except Exception as e:
            safe_tts_speak(f"Error reading text aloud: {str(e)}", self)

    def save_extracted_text(self):
        """Save extracted text to a file"""
        if not hasattr(self, 'extracted_text') or not self.extracted_text.strip():
            safe_tts_speak("No text available to save.", self)
            return

        try:
            # Generate filename based on PDF name
            if hasattr(self, 'current_pdf_path') and self.current_pdf_path:
                base_name = os.path.splitext(os.path.basename(self.current_pdf_path))[0]
                default_filename = f"{base_name}_extracted.txt"
            else:
                default_filename = "pdf_extracted_text.txt"

            # Ask user where to save
            save_path = filedialog.asksaveasfilename(
                title="Save Extracted Text",
                defaultextension=".txt",
                initialvalue=default_filename,
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if save_path:
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(self.extracted_text)

                safe_tts_speak(f"Text saved to {os.path.basename(save_path)}", self)

        except Exception as e:
            safe_tts_speak(f"Error saving text: {str(e)}", self)

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    # Request administrator privileges before starting the application
    if not request_admin_privileges():
        print("Failed to obtain administrator privileges. Some features may not work properly.")
        messagebox.showwarning("Administrator Privileges",
                             "AIVI could not obtain administrator privileges.\n\n"
                             "Some system applications (Narrator, On-Screen Keyboard, etc.) may not launch properly.\n\n"
                             "Please right-click on AIVI and select 'Run as administrator' for full functionality.")

    try:
        app = ModernAIVIGUI()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Application failed to start: {str(e)}")
