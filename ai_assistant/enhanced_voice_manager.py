"""
Enhanced Voice Manager with Offline Support
Handles voice recognition, commands, and audio feedback
"""

import speech_recognition as sr
import logging
import threading
import time
import winsound  # For Windows beep sounds
import os
from typing import Dict, Any, Optional, Callable, List
from .offline_manager import OfflineDataManager
from .tts import TTSManager
from .vi_learning_system import VILearningSystem

class EnhancedVoiceManager:
    def __init__(self, offline_data_manager: OfflineDataManager = None):
        """Initialize enhanced voice manager"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_manager = TTSManager()
        self.offline_data = offline_data_manager or OfflineDataManager()
        self.vi_learning = VILearningSystem(self.offline_data)
        self.is_listening = False
        self.commands = {}
        self.conversation_history = []
        
        # Voice settings
        self.listen_timeout = 15  # 15 seconds as requested
        self.wake_words = ["hey aivi", "aivi", "assistant", "computer"]
        self.exit_words = ["stop listening", "exit", "goodbye", "quit"]
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Calibrate microphone
        self._calibrate_microphone()
        
        # Register offline commands
        self._register_offline_commands()
        
        self.logger.info("Enhanced Voice Manager initialized")

    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            # Configure recognizer for quick response
            self.recognizer.pause_threshold = 0.8  # Quick response - 0.8 seconds of silence
            self.recognizer.energy_threshold = 300  # Adjust sensitivity

            with self.microphone as source:
                self.logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                self.logger.info("Microphone calibrated successfully")
        except Exception as e:
            self.logger.error(f"Failed to calibrate microphone: {e}")

    def _register_offline_commands(self):
        """Register offline voice commands including VI learning system"""
        self.commands = {
            # VI Learning System Commands (Priority)
            "list subjects": self._handle_list_subjects,
            "show subjects": self._handle_list_subjects,
            "available subjects": self._handle_list_subjects,
            "what subjects": self._handle_list_subjects,

            "learn": self._handle_learn_subject,
            "study": self._handle_learn_subject,
            "start learning": self._handle_learn_subject,

            "select": self._handle_select_topic,
            "choose": self._handle_select_topic,
            "option": self._handle_select_topic,

            "repeat": self._handle_repeat,
            "repeat menu": self._handle_repeat,
            "repeat tutorial": self._handle_repeat,
            "say again": self._handle_repeat,

            "back": self._handle_back,
            "go back": self._handle_back,
            "previous": self._handle_back,

            "next topic": self._handle_next_topic,
            "continue": self._handle_next_topic,

            # Search commands
            "search": self._handle_search_vi,
            "find": self._handle_search_vi,
            "look up": self._handle_search_vi,
            "what is": self._handle_search_vi,
            "explain": self._handle_search_vi,
            "define": self._handle_search_vi,
            "tell me about": self._handle_search_vi,

            # Knowledge management
            "remember": self._handle_remember,
            "save": self._handle_remember,
            "add to knowledge": self._handle_remember,

            # System commands
            "status": self._get_system_status,
            "statistics": self._get_data_statistics,
            "help": self._handle_vi_help,
            "commands": self._handle_vi_help,

            # Navigation commands
            "stop listening": self._stop_listening,
            "exit": self._stop_listening,
            "goodbye": self._stop_listening,
            "quit": self._stop_listening,
        }

    def play_ready_beep(self):
        """Play beep sound to indicate microphone is ready"""
        try:
            # Play ascending beep pattern
            winsound.Beep(800, 200)  # First beep
            time.sleep(0.1)
            winsound.Beep(1000, 200)  # Second beep (higher pitch)
        except Exception as e:
            self.logger.warning(f"Could not play beep sound: {e}")
            # Fallback: speak ready indication
            self._speak("Ready")

    def play_listening_beep(self):
        """Play beep to indicate start of listening"""
        try:
            winsound.Beep(1200, 300)  # High pitch, longer duration
        except Exception as e:
            self.logger.warning(f"Could not play listening beep: {e}")

    def play_processing_beep(self):
        """Play beep to indicate processing"""
        try:
            winsound.Beep(600, 150)  # Lower pitch, short
        except Exception as e:
            self.logger.warning(f"Could not play processing beep: {e}")

    def play_error_beep(self):
        """Play error beep pattern"""
        try:
            winsound.Beep(400, 200)
            time.sleep(0.1)
            winsound.Beep(400, 200)
        except Exception as e:
            self.logger.warning(f"Could not play error beep: {e}")

    def _speak(self, text: str):
        """Speak text using TTS"""
        try:
            from .tts import speak_text
            speak_text(text)
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
            print(f"[AIVI]: {text}")

    def listen_for_commands(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Listen for voice commands with beep feedback
        
        Args:
            timeout: Maximum time to listen
            
        Returns:
            Recognized text or None
        """
        try:
            # Play ready beep
            self.play_ready_beep()
            
            with self.microphone as source:
                self.logger.info("Listening for commands...")
                self.play_listening_beep()
                
                # Listen with timeout
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout or self.listen_timeout, 
                    phrase_time_limit=10
                )
                
            # Play processing beep
            self.play_processing_beep()
            
            # Recognize speech
            try:
                text = self.recognizer.recognize_google(audio).lower()
                self.logger.info(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                self.logger.warning("Could not understand audio")
                self.play_error_beep()
                self._speak("Sorry, I didn't understand that.")
                return None
            except sr.RequestError as e:
                # Try offline recognition if available
                try:
                    text = self.recognizer.recognize_sphinx(audio).lower()
                    self.logger.info(f"Recognized offline: {text}")
                    return text
                except:
                    self.logger.error(f"Speech recognition error: {e}")
                    self.play_error_beep()
                    self._speak("Speech recognition is not available.")
                    return None
                
        except sr.WaitTimeoutError:
            self.logger.info("Listening timeout reached")
            return None
        except Exception as e:
            self.logger.error(f"Error listening for commands: {e}")
            self.play_error_beep()
            return None

    def process_command(self, text: str) -> Dict[str, Any]:
        """
        Process recognized voice command offline-first
        
        Args:
            text: Recognized text from voice
            
        Returns:
            Dictionary containing command result
        """
        text = text.lower().strip()
        
        # Record user interaction
        self.offline_data.record_user_interaction(
            text, "", "voice_command", keywords=text.split()
        )
        
        # Find matching command
        for command, handler in self.commands.items():
            if command in text:
                # Extract the query part after the command
                query = text.replace(command, "").strip()
                result = handler(query, text)
                
                # Record the interaction result
                self.offline_data.record_user_interaction(
                    text, 
                    result.get('response', ''), 
                    'voice_response',
                    satisfaction=1 if result.get('success') else 0
                )
                
                return result
        
        # If no specific command found, treat as search
        return self._handle_offline_search(text, text)

    def _handle_offline_search(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle offline search requests"""
        if not query.strip():
            self._speak("What would you like me to search for?")
            return {"success": False, "error": "No search query provided"}
        
        self._speak("Searching offline knowledge base...")
        
        # Search offline data first
        results = self.offline_data.search_offline_data(query)
        
        if results:
            # Use the best result
            best_result = results[0]
            response = f"Based on my offline knowledge: {best_result['answer']}"
            self._speak(response)
            
            return {
                "success": True,
                "response": response,
                "source": "offline",
                "confidence": best_result['confidence'],
                "results_count": len(results)
            }
        else:
            # Check cache
            cached_result = self.offline_data.get_search_cache(query)
            if cached_result:
                response = f"From my search history: {cached_result['response']}"
                self._speak(response)
                return {
                    "success": True,
                    "response": response,
                    "source": "cache",
                    "cached": True
                }
            
            # No offline results available
            self._speak("I don't have information about that in my offline knowledge. Would you like me to search online?")
            return {
                "success": False,
                "error": "No offline results found",
                "response": "No offline information available",
                "suggestion": "online_search_available"
            }

    def _handle_remember(self, content: str, full_text: str) -> Dict[str, Any]:
        """Handle learning/remembering new information"""
        if not content.strip():
            self._speak("What would you like me to remember?")
            return {"success": False, "error": "No content to remember"}
        
        # Parse the content (simple format: "remember that X is Y")
        if " is " in content:
            parts = content.split(" is ", 1)
            if len(parts) == 2:
                question = f"What is {parts[0].strip()}?"
                answer = parts[1].strip()
                keywords = parts[0].strip().split()
                
                success = self.offline_data.add_knowledge_entry(
                    category="user_defined",
                    question=question,
                    answer=answer,
                    keywords=keywords,
                    source="user_input"
                )
                
                if success:
                    self._speak(f"I've remembered that {parts[0]} is {parts[1]}")
                    return {
                        "success": True,
                        "response": f"Remembered: {question} -> {answer}",
                        "action": "knowledge_added"
                    }
        
        # Fallback: store as general knowledge
        success = self.offline_data.add_knowledge_entry(
            category="general",
            question=content,
            answer="User provided information",
            keywords=content.split(),
            source="user_input"
        )
        
        if success:
            self._speak("I've saved that information.")
            return {
                "success": True,
                "response": f"Saved: {content}",
                "action": "information_saved"
            }
        else:
            self._speak("Sorry, I couldn't save that information.")
            return {"success": False, "error": "Failed to save information"}

    def _get_system_status(self, query: str, full_text: str) -> Dict[str, Any]:
        """Get system status"""
        stats = self.offline_data.get_statistics()
        
        status_text = f"System status: I have {stats.get('knowledge_entries', 0)} knowledge entries, " \
                     f"{stats.get('cached_searches', 0)} cached searches, and " \
                     f"{stats.get('user_interactions', 0)} recorded interactions."
        
        self._speak(status_text)
        
        return {
            "success": True,
            "response": status_text,
            "stats": stats
        }

    def _get_data_statistics(self, query: str, full_text: str) -> Dict[str, Any]:
        """Get detailed data statistics"""
        stats = self.offline_data.get_statistics()
        
        categories = ", ".join(stats.get('categories', []))
        most_accessed = stats.get('most_accessed', [])
        
        stats_text = f"Data statistics: {len(stats.get('categories', []))} categories including {categories}. "
        
        if most_accessed:
            stats_text += f"Most accessed query: {most_accessed[0]['query']}"
        
        self._speak(stats_text)
        
        return {
            "success": True,
            "response": stats_text,
            "detailed_stats": stats
        }

    def _show_help(self, query: str, full_text: str) -> Dict[str, Any]:
        """Show available commands"""
        help_text = "Available commands include: search, find, what is, explain, remember, learn, " \
                   "status, statistics, help, and stop listening."
        
        self._speak(help_text)
        
        return {
            "success": True,
            "response": help_text,
            "commands": list(self.commands.keys())
        }

    def _list_commands(self, query: str, full_text: str) -> Dict[str, Any]:
        """List all available commands"""
        commands = ", ".join(self.commands.keys())
        response = f"Available commands: {commands}"
        
        self._speak(response)
        
        return {
            "success": True,
            "response": response,
            "commands": list(self.commands.keys())
        }

    def _stop_listening(self, query: str, full_text: str) -> Dict[str, Any]:
        """Stop listening for commands"""
        self.is_listening = False
        self._speak("Goodbye!")
        return {"success": True, "action": "stop_listening"}

    def start_continuous_listening(self):
        """Start continuous listening with enhanced feedback"""
        self.is_listening = True
        listening_thread = threading.Thread(target=self._continuous_listen_loop)
        listening_thread.daemon = True
        listening_thread.start()
        self.logger.info("Started continuous listening with 15-second timeout")
        self._speak("Voice commands activated. Say my wake word to start.")

    def _continuous_listen_loop(self):
        """Main loop for continuous listening"""
        while self.is_listening:
            try:
                # Listen for wake word with timeout
                text = self.listen_for_commands(timeout=2)  # Short timeout for wake word detection
                
                if text:
                    # Check for exit words
                    if any(exit_word in text.lower() for exit_word in self.exit_words):
                        self._stop_listening("", text)
                        break
                    
                    # Check for wake word
                    if any(wake_word in text.lower() for wake_word in self.wake_words):
                        self._speak("Yes, how can I help you?")
                        
                        # Listen for the actual command with full timeout
                        command_text = self.listen_for_commands(timeout=self.listen_timeout)
                        if command_text:
                            result = self.process_command(command_text)
                            self.logger.info(f"Command result: {result.get('success', False)}")
                        else:
                            self._speak("I didn't hear a command. Try again.")
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                self.logger.error(f"Error in continuous listening loop: {e}")
                self.play_error_beep()
                time.sleep(1)

    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        self.logger.info("Stopped continuous listening")

    def stop(self):
        """Alias for stop_listening() for backward compatibility"""
        self.stop_listening()

    def listen_for_command(self, timeout: Optional[float] = None) -> Optional[str]:
        """Alias for listen_for_commands() for backward compatibility"""
        return self.listen_for_commands(timeout)

    def register_custom_command(self, command: str, handler: Callable):
        """Register a custom command"""
        self.commands[command.lower()] = handler
        self.logger.info(f"Registered custom command: {command}")

    def get_available_commands(self) -> List[str]:
        """Get list of available commands"""
        return list(self.commands.keys())

    def set_listen_timeout(self, timeout: int):
        """Set the listening timeout"""
        self.listen_timeout = timeout
        self.logger.info(f"Listen timeout set to {timeout} seconds")

    def add_wake_word(self, wake_word: str):
        """Add a new wake word"""
        self.wake_words.append(wake_word.lower())
        self.logger.info(f"Added wake word: {wake_word}")

    def export_voice_data(self, export_path: str) -> bool:
        """Export voice interaction data"""
        return self.offline_data.export_data(export_path)

    # ==================== VI Learning System Handlers ====================

    def _handle_list_subjects(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle 'list subjects' command"""
        message = self.vi_learning.list_available_subjects()
        return {
            "success": True,
            "response": message,
            "action": "list_subjects"
        }

    def _handle_learn_subject(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle 'learn [subject]' command"""
        # Extract subject name from command
        subject_name = query.strip()
        if not subject_name:
            # Try to extract from full text
            for keyword in ["learn", "study", "start learning"]:
                if keyword in full_text:
                    subject_name = full_text.replace(keyword, "").strip()
                    break

        if not subject_name:
            self._speak("What subject would you like to learn? Say 'List subjects' to hear available subjects.")
            return {"success": False, "error": "No subject specified"}

        return self.vi_learning.start_learning_subject(subject_name)

    def _handle_select_topic(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle 'select [option]' command"""
        selection = query.strip()
        if not selection:
            selection = full_text

        return self.vi_learning.select_topic(selection)

    def _handle_repeat(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle 'repeat' command"""
        return self.vi_learning.repeat_current_content()

    def _handle_back(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle 'back' command"""
        return self.vi_learning.go_back()

    def _handle_next_topic(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle 'next topic' command"""
        # Get current topic index and move to next
        if self.vi_learning.available_topics and self.vi_learning.current_topic:
            try:
                current_index = self.vi_learning.available_topics.index(self.vi_learning.current_topic)
                if current_index < len(self.vi_learning.available_topics) - 1:
                    next_topic = self.vi_learning.available_topics[current_index + 1]
                    return self.vi_learning.start_tutorial(next_topic)
                else:
                    self._speak("You've reached the end of topics. Say 'Back to topics' to select another topic.")
                    return {"success": False, "message": "Last topic reached"}
            except ValueError:
                pass

        self._speak("Please select a topic first. Say 'Back' to return to the topic menu.")
        return {"success": False, "message": "No current topic"}

    def _handle_search_vi(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle search commands with VI-friendly results"""
        search_query = query.strip()
        if not search_query:
            # Extract search query from full text
            for keyword in ["search", "find", "look up", "what is", "explain", "define", "tell me about"]:
                if keyword in full_text:
                    search_query = full_text.replace(keyword, "").strip()
                    break

        if not search_query:
            self._speak("What would you like to search for?")
            return {"success": False, "error": "No search query"}

        return self.vi_learning.search_and_present(search_query)

    def _handle_vi_help(self, query: str, full_text: str) -> Dict[str, Any]:
        """Handle help command with VI-specific guidance"""
        message = self.vi_learning.provide_help()
        return {
            "success": True,
            "response": message,
            "action": "help_provided"
        }

    def get_vi_learning_state(self) -> Dict[str, Any]:
        """Get current VI learning system state"""
        return self.vi_learning.get_current_state()