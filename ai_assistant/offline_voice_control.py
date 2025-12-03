"""
Offline Voice Control System for AIVI
Uses offline speech recognition and voice commands without internet
"""

import os
import sys
import time
import threading
import queue
import re
from collections import defaultdict

# Try to import offline speech recognition libraries
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("speech_recognition not available. Install with: pip install SpeechRecognition")

try:
    import pocketsphinx
    POCKETSPHINX_AVAILABLE = True
except ImportError:
    POCKETSPHINX_AVAILABLE = False
    print("pocketsphinx not available. Install with: pip install pocketsphinx")

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print("pyaudio not available. Install with: pip install pyaudio")

# Import our modules
from . import desktop_control

class OfflineVoiceController:
    def __init__(self):
        self.is_listening = False
        self.command_queue = queue.Queue()
        self.recognizer = None
        self.microphone = None
        self.listen_thread = None

        # Initialize if libraries are available
        if SPEECH_RECOGNITION_AVAILABLE and PYAUDIO_AVAILABLE:
            self.setup_recognizer()

        # Offline command patterns and responses
        self.command_patterns = self.setup_command_patterns()
        self.setup_offline_responses()

    def setup_recognizer(self):
        """Setup offline speech recognizer"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()

            # Adjust for ambient noise
            print("[Offline Voice] Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)

            print("[Offline Voice] Voice control ready!")
            return True
        except Exception as e:
            print(f"[Offline Voice] Setup failed: {e}")
            return False

    def setup_command_patterns(self):
        """Setup offline command patterns for voice recognition"""
        return {
            # Application commands
            'open_word': [
                r'open\s+(microsoft\s+)?word',
                r'start\s+(microsoft\s+)?word',
                r'launch\s+(microsoft\s+)?word'
            ],
            'open_calculator': [
                r'open\s+calculator',
                r'start\s+calculator',
                r'launch\s+calculator',
                r'open\s+calc'
            ],
            'open_notepad': [
                r'open\s+notepad',
                r'start\s+notepad',
                r'launch\s+notepad'
            ],
            'open_browser': [
                r'open\s+(google\s+)?chrome',
                r'open\s+browser',
                r'start\s+browser',
                r'launch\s+browser'
            ],
            'open_file_explorer': [
                r'open\s+file\s+explorer',
                r'open\s+explorer',
                r'show\s+files',
                r'open\s+files'
            ],

            # System commands
            'take_screenshot': [
                r'take\s+(a\s+)?screenshot',
                r'capture\s+screen',
                r'screenshot'
            ],
            'open_settings': [
                r'open\s+settings',
                r'system\s+settings',
                r'control\s+panel'
            ],

            # Accessibility commands
            'start_narrator': [
                r'start\s+narrator',
                r'enable\s+narrator',
                r'turn\s+on\s+narrator'
            ],
            'start_magnifier': [
                r'start\s+magnifier',
                r'enable\s+magnifier',
                r'zoom\s+screen'
            ],
            'show_keyboard': [
                r'show\s+keyboard',
                r'virtual\s+keyboard',
                r'on\s+screen\s+keyboard'
            ],

            # AIVI specific commands
            'voice_settings': [
                r'voice\s+settings',
                r'speech\s+settings',
                r'open\s+voice\s+settings'
            ],
            'pdf_reader': [
                r'pdf\s+reader',
                r'open\s+pdf\s+reader',
                r'read\s+pdf'
            ],
            'help': [
                r'help',
                r'what\s+can\s+you\s+do',
                r'show\s+help',
                r'commands'
            ],

            # Control commands
            'stop_listening': [
                r'stop\s+listening',
                r'end\s+conversation',
                r'stop\s+voice',
                r'turn\s+off\s+voice'
            ]
        }

    def setup_offline_responses(self):
        """Setup offline responses for commands"""
        self.responses = {
            'open_word': "Opening Microsoft Word",
            'open_calculator': "Opening Calculator",
            'open_notepad': "Opening Notepad",
            'open_browser': "Opening web browser",
            'open_file_explorer': "Opening File Explorer",
            'take_screenshot': "Taking screenshot",
            'open_settings': "Opening system settings",
            'start_narrator': "Starting Narrator",
            'start_magnifier': "Starting Magnifier",
            'show_keyboard': "Showing on-screen keyboard",
            'voice_settings': "Opening voice settings",
            'pdf_reader': "Opening PDF reader",
            'help': "Here are the available voice commands",
            'unknown': "I didn't understand that command. Say 'help' for available commands.",
            'error': "There was an error processing your command",
            'listening': "I'm listening for your command",
            'not_available': "Voice recognition is not available in offline mode. Please install required libraries."
        }

    def recognize_speech_offline(self, audio_data):
        """Recognize speech using offline methods"""
        try:
            # Try offline recognition with PocketSphinx
            if POCKETSPHINX_AVAILABLE:
                text = self.recognizer.recognize_sphinx(audio_data)
                return text.lower().strip()
        except Exception as e:
            print(f"[Offline Voice] PocketSphinx recognition failed: {e}")

        # Fallback: Try basic pattern matching with Whisper if available
        try:
            import whisper
            # Note: This would require Whisper model to be downloaded
            # For now, we'll use a simpler approach
            pass
        except ImportError:
            pass

        return None

    def match_command_pattern(self, text):
        """Match recognized text to command patterns"""
        if not text:
            return None

        text = text.lower().strip()

        for command, patterns in self.command_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return command

        return None

    def execute_offline_command(self, command, recognized_text=""):
        """Execute offline voice command"""
        try:
            if command == 'open_word':
                return desktop_control.open_app('word')
            elif command == 'open_calculator':
                return desktop_control.open_app('calculator')
            elif command == 'open_notepad':
                return desktop_control.open_app('notepad')
            elif command == 'open_browser':
                return desktop_control.open_app('chrome')
            elif command == 'open_file_explorer':
                return desktop_control.open_app('file_explorer')
            elif command == 'take_screenshot':
                return desktop_control.take_screenshot()
            elif command == 'open_settings':
                return desktop_control.open_app('control_panel')
            elif command == 'start_narrator':
                return desktop_control.enable_accessibility('narrator')
            elif command == 'start_magnifier':
                return desktop_control.enable_accessibility('magnifier')
            elif command == 'show_keyboard':
                return desktop_control.enable_accessibility('onscreen_keyboard')
            elif command == 'help':
                return True, self.get_help_message()
            elif command == 'stop_listening':
                self.stop_listening()
                return True, "Voice control stopped"
            else:
                return False, "Command not recognized"

        except Exception as e:
            print(f"[Offline Voice] Command execution error: {e}")
            return False, f"Error executing command: {str(e)}"

    def get_help_message(self):
        """Get offline help message"""
        return """Available offline voice commands:

📱 APPLICATIONS:
• "Open Word" - Microsoft Word
• "Open Calculator" - Calculator
• "Open Notepad" - Notepad
• "Open Browser" - Web Browser
• "Open File Explorer" - File Manager

🖥️ SYSTEM:
• "Take Screenshot" - Capture screen
• "Open Settings" - System settings

♿ ACCESSIBILITY:
• "Start Narrator" - Screen reader
• "Start Magnifier" - Screen zoom
• "Show Keyboard" - Virtual keyboard

🎯 AIVI FEATURES:
• "Voice Settings" - Voice configuration
• "PDF Reader" - PDF document reader
• "Help" - Show this help

🔧 CONTROL:
• "Stop Listening" - End voice control

Say any command clearly and wait for response."""

    def listen_for_commands(self, callback=None):
        """Start listening for offline voice commands"""
        if not SPEECH_RECOGNITION_AVAILABLE or not PYAUDIO_AVAILABLE:
            print("[Offline Voice] Required libraries not available")
            if callback:
                callback("not_available", "")
            return

        self.is_listening = True

        def listen_loop():
            print("[Offline Voice] Starting offline voice control...")
            print("[Offline Voice] Say 'help' for available commands")
            print("[Offline Voice] Say 'stop listening' to end")

            while self.is_listening:
                try:
                    with self.microphone as source:
                        print("[Offline Voice] Listening...")
                        # Listen for audio
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)

                        # Try offline recognition
                        recognized_text = self.recognize_speech_offline(audio)

                        if recognized_text:
                            print(f"[Offline Voice] Recognized: {recognized_text}")

                            # Match to command pattern
                            command = self.match_command_pattern(recognized_text)

                            if command:
                                print(f"[Offline Voice] Executing: {command}")
                                success, message = self.execute_offline_command(command, recognized_text)

                                if callback:
                                    callback(command, message)
                                else:
                                    print(f"[Offline Voice] Result: {message}")

                                if command == 'stop_listening':
                                    break
                            else:
                                print("[Offline Voice] Command not recognized")
                                if callback:
                                    callback("unknown", self.responses['unknown'])

                except sr.WaitTimeoutError:
                    # Continue listening
                    continue
                except sr.UnknownValueError:
                    # Could not understand audio
                    continue
                except Exception as e:
                    print(f"[Offline Voice] Error: {e}")
                    time.sleep(0.5)

            print("[Offline Voice] Stopped listening")

        # Start listening in separate thread
        self.listen_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listen_thread.start()

    def stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=1)

    def is_available(self):
        """Check if offline voice control is available"""
        return SPEECH_RECOGNITION_AVAILABLE and PYAUDIO_AVAILABLE

# Global instance
offline_voice_controller = OfflineVoiceController()

# Convenience functions
def start_offline_voice_control(callback=None):
    """Start offline voice control"""
    if offline_voice_controller.is_available():
        offline_voice_controller.listen_for_commands(callback)
        return True
    else:
        print("[Offline Voice] Voice control not available. Install: pip install SpeechRecognition pocketsphinx pyaudio")
        return False

def stop_offline_voice_control():
    """Stop offline voice control"""
    offline_voice_controller.stop_listening()

def is_offline_voice_available():
    """Check if offline voice control is available"""
    return offline_voice_controller.is_available()

def get_offline_voice_help():
    """Get help for offline voice commands"""
    return offline_voice_controller.get_help_message()