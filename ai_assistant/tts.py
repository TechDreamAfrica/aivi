"""
Text-to-Speech (TTS) module
"""
import time

def play_beep(frequency=1000, duration=200):
    """
    Play a system beep sound for VI accessibility

    Args:
        frequency (int): Frequency in Hz (default: 1000)
        duration (int): Duration in milliseconds (default: 200)
    """
    try:
        import winsound
        winsound.Beep(frequency, duration)
    except (ImportError, RuntimeError) as e:
        # winsound not available on non-Windows systems or in certain environments
        print(f"[Beep] {frequency}Hz for {duration}ms (audio not available: {type(e).__name__})")
    except Exception as e:
        print(f"[Beep] Error playing beep: {e}")

def play_ready_signal():
    """
    Play a two-tone beep to signal system is ready for VI students
    """
    play_beep(1000, 200)
    time.sleep(0.1)
    play_beep(1200, 150)

def play_success_beep():
    """
    Play a success confirmation beep
    """
    play_beep(800, 100)

def play_error_beep():
    """
    Play an error notification beep (lower tone)
    """
    play_beep(400, 300)

class TTSManager:
    """Thread-safe TTS manager to handle voice settings and speech synthesis"""
    def __init__(self):
        self.current_voice_mode = 'default'
        self._lock = None
        
    def _get_lock(self):
        """Lazy initialization of threading lock"""
        if self._lock is None:
            import threading
            self._lock = threading.Lock()
        return self._lock
    
    def set_voice_mode(self, mode):
        """Thread-safe voice mode setter"""
        with self._get_lock():
            self.current_voice_mode = mode
    
    def get_voice_mode(self):
        """Thread-safe voice mode getter"""
        with self._get_lock():
            return self.current_voice_mode

    def speak(self, text, voice='default', speed=1.0):
        """Speak text using TTS"""
        speak_text(text, voice, speed)

# Create TTS class alias for backward compatibility
class TTS:
    """TTS class for compatibility"""
    def __init__(self):
        self.manager = TTSManager()
    
    def speak(self, text, voice='default', speed=1.0):
        """Speak text"""
        self.manager.speak(text, voice, speed)
    
    def set_voice_mode(self, mode):
        """Set voice mode"""
        self.manager.set_voice_mode(mode)
    
    def get_voice_mode(self):
        """Get voice mode"""
        return self.manager.get_voice_mode()

# Global TTS manager instance
_tts_manager = TTSManager()

def set_voice_mode(mode):
    """
    Set the voice mode for TTS
    
    Args:
        mode (str): Voice mode - 'default', 'male', 'female', or 'custom'
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if mode.lower() == 'male':
            # Try to find a male voice
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                    _tts_manager.set_voice_mode(voice.id)
                    return True
            # Fallback to first available voice
            if voices:
                _tts_manager.set_voice_mode(voices[0].id)
                return True
        elif mode.lower() == 'female':
            # Try to find a female voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower() or 'hazel' in voice.name.lower():
                    _tts_manager.set_voice_mode(voice.id)
                    return True
            # Fallback to second available voice if exists
            if len(voices) > 1:
                _tts_manager.set_voice_mode(voices[1].id)
                return True
        elif mode.lower() == 'default':
            _tts_manager.set_voice_mode('default')
            return True
        else:  # custom or other
            _tts_manager.set_voice_mode(mode)
            return True
            
    except ImportError:
        print("TTS not available: pyttsx3 module not found")
        return False
    except Exception as e:
        print(f"Could not set voice mode: {e}")
        return False
    
    return False

def get_voice_mode():
    """Get the current voice mode"""
    return _tts_manager.get_voice_mode()

def speak_text(text, voice='default', speed=1.0, pitch=1.0, language='en'):
    """
    Speak text using TTS engine (requires pyttsx3)
    Falls back silently if TTS is not available
    
    Args:
        text (str): Text to speak
        voice (str): Voice to use ('default', 'male', 'female', or specific voice ID)
        speed (float): Speech rate multiplier (default: 1.0)
        pitch (float): Pitch adjustment (not implemented in pyttsx3)
        language (str): Language code (not implemented in pyttsx3)
    """
    if not text or not text.strip():
        return
        
    try:
        # Real TTS using pyttsx3 (offline, supports speed and voice selection)
        import pyttsx3
        engine = pyttsx3.init()
        
        # Set properties if available
        try:
            # Set speech rate (words per minute)
            rate = engine.getProperty('rate')
            engine.setProperty('rate', int(rate * speed))
            
            # Use current voice mode if voice is default
            current_mode = _tts_manager.get_voice_mode()
            if voice == 'default' and current_mode != 'default':
                engine.setProperty('voice', current_mode)
            elif voice != 'default':
                # Handle voice presets
                if voice.lower() in ['male', 'female']:
                    _tts_manager.set_voice_mode(voice)
                    engine.setProperty('voice', _tts_manager.get_voice_mode())
                else:
                    engine.setProperty('voice', voice)
                
            # Set volume (0.0 to 1.0)
            engine.setProperty('volume', min(1.0, max(0.0, 1.0)))
            
        except Exception as e:
            print(f"[TTS] Warning: Could not set voice properties: {e}")
            pass
            
        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
        print(f"[TTS] Spoke: {text[:50]}{'...' if len(text) > 50 else ''}")
        
    except ImportError:
        # pyttsx3 not available, skip TTS
        print(f"[TTS] Text-to-speech not available: {text}")
        pass
    except Exception as e:
        # Other TTS errors
        print(f"[TTS] Error: {e}")
        pass

def get_available_voices():
    """
    Get list of available voices on the system
    
    Returns:
        list: List of dictionaries containing voice information
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        voice_list = []
        for i, voice in enumerate(voices):
            voice_info = {
                'id': voice.id,
                'name': voice.name,
                'age': getattr(voice, 'age', None),
                'gender': getattr(voice, 'gender', None),
                'languages': getattr(voice, 'languages', []),
                'index': i
            }
            voice_list.append(voice_info)
        
        return voice_list
        
    except ImportError:
        print("[TTS] pyttsx3 not available for voice listing")
        return []
    except Exception as e:
        print(f"[TTS] Error getting voices: {e}")
        return []

def stop_speaking():
    """
    Stop current speech (if supported by TTS engine)
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.stop()
        print("[TTS] Speech stopped")
    except ImportError:
        print("[TTS] pyttsx3 not available for stopping speech")
    except Exception as e:
        print(f"[TTS] Error stopping speech: {e}")

def test_tts():
    """
    Test TTS functionality with a sample message
    """
    print("Testing TTS functionality...")
    
    # Test basic speech
    speak_text("Hello! This is a test of the text to speech system.")
    
    # Test voice listing
    voices = get_available_voices()
    print(f"Available voices: {len(voices)}")
    for voice in voices[:3]:  # Show first 3 voices
        print(f"  - {voice['name']} ({voice['gender']})")
    
    # Test different speeds
    speak_text("This is normal speed.", speed=1.0)
    speak_text("This is faster speech.", speed=1.5)
    speak_text("This is slower speech.", speed=0.7)
    
    print("TTS test completed!")

def speak_async(text, voice='default', speed=1.0):
    """
    Speak text asynchronously in a separate thread
    
    Args:
        text (str): Text to speak
        voice (str): Voice to use
        speed (float): Speech rate multiplier
    """
    import threading
    
    def speak_worker():
        speak_text(text, voice, speed)
    
    thread = threading.Thread(target=speak_worker, daemon=True)
    thread.start()
    return thread
