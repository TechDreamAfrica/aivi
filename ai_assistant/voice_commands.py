"""
Voice-Activated Commands and Navigation module
Enhanced for comprehensive desktop control and conversation
"""

import speech_recognition as sr
import time
import threading
from . import desktop_control
import winsound

def play_ready_beep():
    """
    Play a beep sound to signal microphone is ready for VI students
    Uses system beep (frequency: 1000 Hz, duration: 200ms)
    """
    try:
        # Play a friendly beep sound (1000 Hz for 200 milliseconds)
        winsound.Beep(1000, 200)
        time.sleep(0.1)  # Small pause
        # Play a second shorter beep to confirm
        winsound.Beep(1200, 150)
    except Exception as e:
        print(f"[Voice] Could not play beep: {e}")

def listen_for_command():
    """
    Enhanced voice command recognition for VI students
    - Plays beep when ready
    - Quick response after speech ends
    """
    recognizer = sr.Recognizer()

    # Configure recognizer for better VI accessibility
    recognizer.pause_threshold = 0.8  # Quick response - 0.8 seconds of silence
    recognizer.energy_threshold = 300  # Adjust sensitivity

    with sr.Microphone() as source:
        print("[Voice] Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Play beep to signal microphone is ready
        print("[Voice] Microphone ready - Playing beep signal")
        play_ready_beep()

        print("[Voice] Listening for command... Speak now.")

        try:
            # Listen with reasonable timeout and phrase limit
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)

            print("[Voice] Processing your command...")
            command = recognizer.recognize_google(audio)
            print(f"[Voice] Recognized: {command}")

            # Play confirmation beep
            winsound.Beep(800, 100)

            return command
        except sr.WaitTimeoutError:
            print("[Voice] Timeout. No speech detected.")
            winsound.Beep(400, 300)  # Low beep for error
            return ""
        except sr.UnknownValueError:
            print("[Voice] Could not understand audio.")
            winsound.Beep(400, 300)  # Low beep for error
            return ""
        except Exception as e:
            print(f"[Voice] Error: {e}")
            winsound.Beep(400, 300)  # Low beep for error
            return ""

def listen_for_continuous_conversation(callback=None):
    """
    Continuous listening for natural conversation
    Enhanced for VI students with beep signals
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Configure recognizer for VI accessibility
    recognizer.pause_threshold = 0.8  # Quick response - 0.8 seconds of silence

    print("[Voice] Starting continuous conversation mode...")
    print("[Voice] Say 'stop listening' to end.")

    # Adjust for ambient noise
    with microphone as source:
        print("[Voice] Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    # Play ready beep
    print("[Voice] Ready - Playing beep signal")
    play_ready_beep()

    stop_listening = False

    def listen_loop():
        nonlocal stop_listening
        while not stop_listening:
            try:
                # Play a subtle ready beep before each listening cycle
                winsound.Beep(900, 80)

                with microphone as source:
                    # Listen for audio with reasonable timeout
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                    text = recognizer.recognize_google(audio)

                    # Play confirmation beep
                    winsound.Beep(800, 100)
                    
                    if text.lower().strip() in ['stop listening', 'end conversation', 'stop']:
                        print("[Voice] Stopping continuous listening.")
                        stop_listening = True
                        break
                    
                    if callback:
                        callback(text)
                    else:
                        print(f"[Voice] You said: {text}")
                        
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                continue
            except sr.UnknownValueError:
                # Could not understand audio, continue listening
                continue
            except Exception as e:
                print(f"[Voice] Listening error: {e}")
                time.sleep(0.5)
    
    # Start listening in a separate thread
    listen_thread = threading.Thread(target=listen_loop, daemon=True)
    listen_thread.start()
    
    return lambda: setattr(locals(), 'stop_listening', True)

def process_desktop_command(command):
    """
    Process commands related to opening desktop applications
    Returns tuple: (success, message, action_taken)
    """
    command_lower = command.lower()
    
    # Application opening commands
    app_keywords = {
        'word': ['word', 'microsoft word', 'ms word', 'document editor', 'text editor'],
        'powerpoint': ['powerpoint', 'microsoft powerpoint', 'ms powerpoint', 'presentation', 'slides'],
        'excel': ['excel', 'microsoft excel', 'ms excel', 'spreadsheet', 'calculator app'],
        'onenote': ['onenote', 'microsoft onenote', 'ms onenote', 'notes app'],
        'calculator': ['calculator', 'calc', 'math calculator'],
        'notepad': ['notepad', 'text editor', 'simple editor'],
        'wordpad': ['wordpad', 'rich text editor'],
        'narrator': ['narrator', 'screen reader', 'read screen'],
        'magnifier': ['magnifier', 'zoom', 'magnify screen', 'screen zoom'],
        'onscreen_keyboard': ['on screen keyboard', 'virtual keyboard', 'keyboard'],
        'control_panel': ['control panel', 'system settings', 'settings'],
        'file_explorer': ['file explorer', 'explorer', 'files', 'folders'],
        'chrome': ['chrome', 'google chrome', 'browser'],
        'firefox': ['firefox', 'mozilla firefox'],
        'edge': ['edge', 'microsoft edge'],
        'vscode': ['visual studio code', 'vscode', 'code editor'],
        'task_manager': ['task manager', 'processes', 'system monitor']
    }
    
    # Check for "open" commands
    if any(word in command_lower for word in ['open', 'start', 'launch', 'run']):
        for app_name, keywords in app_keywords.items():
            if any(keyword in command_lower for keyword in keywords):
                success, message = desktop_control.open_app(app_name)
                return success, message, f"opened_{app_name}"
    
    # Website opening commands
    if any(word in command_lower for word in ['open', 'go to', 'navigate to']) and any(word in command_lower for word in ['website', 'site', '.com', 'www']):
        # Extract URL from command
        words = command_lower.split()
        for word in words:
            if any(domain in word for domain in ['.com', '.org', '.net', '.edu', '.gov', 'www.']):
                success, message = desktop_control.open_website(word)
                return success, message, "opened_website"
    
    # Folder opening commands
    folder_keywords = {
        'documents': ['documents', 'my documents', 'document folder'],
        'downloads': ['downloads', 'download folder'],
        'desktop': ['desktop', 'desktop folder'],
        'pictures': ['pictures', 'photos', 'image folder'],
        'music': ['music', 'songs', 'audio folder'],
        'videos': ['videos', 'movies', 'video folder']
    }
    
    if any(word in command_lower for word in ['open', 'show', 'navigate to']) and 'folder' in command_lower:
        for folder_name, keywords in folder_keywords.items():
            if any(keyword in command_lower for keyword in keywords):
                shortcuts = desktop_control.quick_shortcuts()
                if folder_name in shortcuts:
                    success, message = shortcuts[folder_name]()
                    return success, message, f"opened_{folder_name}_folder"
    
    # Accessibility commands
    accessibility_keywords = {
        'narrator': ['start narrator', 'enable narrator', 'screen reader on'],
        'magnifier': ['start magnifier', 'enable zoom', 'magnify screen'],
        'on_screen_keyboard': ['show keyboard', 'virtual keyboard', 'on screen keyboard'],
        'high_contrast': ['high contrast', 'enable high contrast', 'contrast mode']
    }
    
    for feature, keywords in accessibility_keywords.items():
        if any(keyword in command_lower for keyword in keywords):
            success, message = desktop_control.enable_accessibility(feature)
            return success, message, f"enabled_{feature}"
    
    return False, "Command not recognized as a desktop control command", "no_action"

def get_conversation_context(command):
    """
    Analyze command to provide context for more natural conversation
    Returns context information for better AI responses
    """
    command_lower = command.lower()
    
    context = {
        'intent': 'unknown',
        'entities': [],
        'emotion': 'neutral',
        'urgency': 'normal',
        'topic': None
    }
    
    # Intent recognition
    if any(word in command_lower for word in ['help', 'assist', 'support']):
        context['intent'] = 'help_request'
    elif any(word in command_lower for word in ['open', 'start', 'launch']):
        context['intent'] = 'action_request'
    elif any(word in command_lower for word in ['what', 'how', 'when', 'where', 'why']):
        context['intent'] = 'information_request'
    elif any(word in command_lower for word in ['thank', 'thanks', 'appreciate']):
        context['intent'] = 'gratitude'
    elif any(word in command_lower for word in ['sorry', 'apologize', 'mistake']):
        context['intent'] = 'apology'
    
    # Emotion detection (basic)
    if any(word in command_lower for word in ['urgent', 'emergency', 'quickly', 'fast']):
        context['urgency'] = 'high'
        context['emotion'] = 'anxious'
    elif any(word in command_lower for word in ['please', 'kindly', 'would you']):
        context['emotion'] = 'polite'
    elif any(word in command_lower for word in ['frustrated', 'angry', 'annoyed']):
        context['emotion'] = 'negative'
    elif any(word in command_lower for word in ['happy', 'glad', 'excited']):
        context['emotion'] = 'positive'
    
    # Topic identification
    if any(word in command_lower for word in ['study', 'learn', 'academic', 'education']):
        context['topic'] = 'academic'
    elif any(word in command_lower for word in ['accessibility', 'vision', 'blind', 'visual']):
        context['topic'] = 'accessibility'
    elif any(word in command_lower for word in ['computer', 'software', 'application', 'program']):
        context['topic'] = 'technology'
    elif any(word in command_lower for word in ['schedule', 'time', 'calendar', 'reminder']):
        context['topic'] = 'time_management'
    
    return context

def start_real_time_transcription():
    """
    Start real-time voice transcription generator
    Enhanced for VI students with beep signals
    Yields transcribed text as it's captured
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Configure for VI accessibility
    recognizer.pause_threshold = 0.8  # Quick response - 0.8 seconds of silence

    print("[Voice] Starting real-time transcription...")
    print("[Voice] Say 'stop transcription' to end.")

    # Adjust for ambient noise
    with microphone as source:
        print("[Voice] Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)

    # Play ready beep
    print("[Voice] Ready - Playing beep signal")
    play_ready_beep()

    try:
        while True:
            with microphone as source:
                try:
                    # Play subtle ready beep before listening
                    winsound.Beep(900, 80)

                    # Listen for audio with reasonable parameters
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                    text = recognizer.recognize_google(audio)

                    # Play confirmation beep
                    winsound.Beep(800, 100)
                    
                    if text.lower() in ['stop transcription', 'end transcription', 'stop']:
                        print("[Voice] Stopping real-time transcription.")
                        break
                        
                    yield text
                    
                except sr.WaitTimeoutError:
                    # No speech detected, continue listening
                    continue
                except sr.UnknownValueError:
                    # Could not understand audio, continue listening
                    continue
                except Exception as e:
                    print(f"[Voice] Transcription error: {e}")
                    break
                    
    except KeyboardInterrupt:
        print("[Voice] Real-time transcription stopped by user.")
    except Exception as e:
        print(f"[Voice] Real-time transcription error: {e}")

def voice_navigation_commands():
    """
    Return a dictionary of voice navigation commands and their descriptions
    """
    return {
        # Desktop Control
        "open_applications": [
            "open word", "start powerpoint", "launch calculator", 
            "open notepad", "start narrator", "show magnifier"
        ],
        "open_folders": [
            "open documents folder", "show downloads", "navigate to desktop",
            "open pictures folder", "show music folder"
        ],
        "accessibility": [
            "start narrator", "enable magnifier", "show on screen keyboard",
            "enable high contrast", "start screen reader"
        ],
        "websites": [
            "open google.com", "go to youtube.com", "navigate to scholar.google.com"
        ],
        
        # Academic Functions
        "academic_help": [
            "help with math", "explain photosynthesis", "what is algebra",
            "define democracy", "how do plants grow"
        ],
        "study_tools": [
            "start quiz mode", "record lecture", "summarize notes",
            "add study event", "set reminder"
        ],
        
        # Accessibility Features
        "text_processing": [
            "read text from image", "convert to braille", "describe scene",
            "transcribe audio", "translate text"
        ],
        "navigation": [
            "where am I", "get current location", "find nearby places"
        ],
        
        # System Control
        "voice_control": [
            "change voice mode", "start real time transcription",
            "enable offline mode", "switch to online mode"
        ]
    }

def get_smart_suggestions(partial_command):
    """
    Provide smart suggestions based on partial voice command
    """
    suggestions = []
    commands = voice_navigation_commands()
    
    partial_lower = partial_command.lower()
    
    for category, command_list in commands.items():
        for command in command_list:
            if any(word in command.lower() for word in partial_lower.split()):
                suggestions.append({
                    'command': command,
                    'category': category,
                    'confidence': len([w for w in partial_lower.split() if w in command.lower()]) / len(partial_lower.split())
                })
    
    # Sort by confidence
    suggestions.sort(key=lambda x: x['confidence'], reverse=True)
    
    return suggestions[:5]  # Return top 5 suggestions
