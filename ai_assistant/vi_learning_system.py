"""
VI Learning System - Comprehensive learning module for Visually Impaired Students
Provides voice-controlled navigation, subject-based learning, and structured tutorials
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from .offline_manager import OfflineDataManager
from .tts import speak_text, play_beep, play_ready_signal, play_success_beep
import time


class VILearningSystem:
    """Manages voice-controlled learning for VI students"""

    def __init__(self, offline_data_manager: OfflineDataManager = None):
        """Initialize VI Learning System"""
        self.offline_data = offline_data_manager or OfflineDataManager()
        self.logger = logging.getLogger(__name__)

        # Current session state
        self.current_subject = None
        self.current_topic = None
        self.available_subjects = []
        self.available_topics = []
        self.learning_mode = None  # 'browse', 'tutorial', 'quiz'

        # Voice navigation state
        self.menu_level = 'main'  # 'main', 'subject', 'topic', 'content'
        self.menu_position = 0

        # Load available subjects from offline data
        self._load_subjects()

        self.logger.info("VI Learning System initialized")

    def _load_subjects(self):
        """Load available subjects from offline knowledge base"""
        try:
            # Get unique categories from knowledge base
            with open(self.offline_data.csv_file, 'r', encoding='utf-8') as f:
                import csv
                reader = csv.DictReader(f)
                categories = set()
                for row in reader:
                    if row['category']:
                        categories.add(row['category'].title())

                self.available_subjects = sorted(list(categories))
                self.logger.info(f"Loaded {len(self.available_subjects)} subjects")
        except Exception as e:
            self.logger.error(f"Error loading subjects: {e}")
            self.available_subjects = []

    def welcome_message(self):
        """Provide welcome message for VI students"""
        play_ready_signal()

        message = """Welcome to AIVI, your AI learning assistant for visually impaired students.

I'm here to help you learn with voice commands.

You can say commands like:
- 'Learn Mathematics' to start learning a subject
- 'List subjects' to hear all available subjects
- 'Help' to hear all commands
- 'Read my notes' to read uploaded documents

I will guide you through menus using voice prompts.
After each option, I'll wait for your response.

Say 'Help' anytime to hear available commands."""

        speak_text(message, speed=0.9)
        return message

    def list_available_subjects(self) -> str:
        """List all available subjects with voice feedback"""
        play_ready_signal()

        if not self.available_subjects:
            message = "No subjects are currently available in the offline database. Please contact your institution to load course materials."
            speak_text(message)
            return message

        message = f"I have {len(self.available_subjects)} subjects available. They are: "
        speak_text(message, speed=0.9)

        for i, subject in enumerate(self.available_subjects, 1):
            subject_line = f"Number {i}: {subject}"
            speak_text(subject_line, speed=0.9)
            time.sleep(0.5)  # Pause between subjects

        prompt = "Say 'Learn' followed by the subject name, or say 'Repeat' to hear the list again."
        speak_text(prompt, speed=0.9)

        return f"Available subjects: {', '.join(self.available_subjects)}"

    def start_learning_subject(self, subject_name: str) -> Dict[str, Any]:
        """Start learning a specific subject"""
        play_ready_signal()

        # Find matching subject
        subject_match = None
        subject_lower = subject_name.lower()

        for subject in self.available_subjects:
            if subject_lower in subject.lower() or subject.lower() in subject_lower:
                subject_match = subject
                break

        if not subject_match:
            message = f"Sorry, I couldn't find the subject '{subject_name}'. Say 'List subjects' to hear available subjects."
            speak_text(message)
            play_beep(400, 300)
            return {
                'success': False,
                'message': message,
                'action': 'subject_not_found'
            }

        # Set current subject
        self.current_subject = subject_match
        self.menu_level = 'subject'

        # Load topics for this subject
        topics = self._load_topics_for_subject(subject_match)
        self.available_topics = topics

        if not topics:
            message = f"I found the subject {subject_match}, but there are no topics available yet. Would you like to search online for {subject_match} content? Say 'Yes' or 'No'."
            speak_text(message)
            return {
                'success': False,
                'message': message,
                'action': 'no_topics_available',
                'subject': subject_match,
                'prompt_online_search': True
            }

        # Announce subject and topics
        message = f"You selected {subject_match}. I found {len(topics)} topics available."
        speak_text(message, speed=0.9)
        time.sleep(0.5)

        self._present_topic_menu(topics)

        return {
            'success': True,
            'message': message,
            'subject': subject_match,
            'topics': topics,
            'action': 'topic_menu_presented'
        }

    def _load_topics_for_subject(self, subject: str) -> List[Dict[str, Any]]:
        """Load all topics for a given subject from offline data"""
        results = self.offline_data.search_offline_data(subject, category=subject.lower())

        # Extract unique topics from results
        topics = []
        seen_questions = set()

        for result in results:
            question = result['question']
            if question not in seen_questions:
                topics.append({
                    'title': question,
                    'content': result['answer'],
                    'keywords': result['keywords'],
                    'confidence': result['confidence']
                })
                seen_questions.add(question)

        return topics

    def _present_topic_menu(self, topics: List[Dict[str, Any]]):
        """Present topic menu with voice prompts"""
        speak_text("Here are the available topics:", speed=0.9)
        time.sleep(0.5)

        for i, topic in enumerate(topics, 1):
            play_beep(900, 80)  # Menu item beep
            topic_line = f"Option {i}: {topic['title']}"
            speak_text(topic_line, speed=0.9)
            time.sleep(0.7)

        time.sleep(0.5)
        prompt = "Say 'Select' followed by the option number, or say 'Repeat menu' to hear again."
        speak_text(prompt, speed=0.9)

    def select_topic(self, selection: str) -> Dict[str, Any]:
        """Select a topic from the menu"""
        play_ready_signal()

        if not self.available_topics:
            message = "No topics are currently loaded. Please select a subject first."
            speak_text(message)
            return {'success': False, 'message': message}

        # Parse selection (could be number or topic name)
        topic_index = None

        # Try to extract number
        import re
        numbers = re.findall(r'\d+', selection)
        if numbers:
            try:
                topic_index = int(numbers[0]) - 1
            except ValueError:
                pass

        # If no number, try to match topic title
        if topic_index is None:
            selection_lower = selection.lower()
            for i, topic in enumerate(self.available_topics):
                if selection_lower in topic['title'].lower():
                    topic_index = i
                    break

        # Validate index
        if topic_index is None or topic_index < 0 or topic_index >= len(self.available_topics):
            message = "Invalid selection. Say 'Repeat menu' to hear the options again."
            speak_text(message)
            play_beep(400, 300)
            return {'success': False, 'message': message}

        # Get selected topic
        topic = self.available_topics[topic_index]
        self.current_topic = topic
        self.menu_level = 'content'

        play_success_beep()

        # Start tutorial
        return self.start_tutorial(topic)

    def start_tutorial(self, topic: Dict[str, Any]) -> Dict[str, Any]:
        """Start a full tutorial on the selected topic"""
        play_ready_signal()

        # Announce topic
        announcement = f"Starting tutorial on: {topic['title']}"
        speak_text(announcement, speed=0.9)
        time.sleep(1)

        # Deliver content in clear, structured way
        speak_text("Here is the lesson:", speed=0.9)
        time.sleep(0.5)

        # Split content into paragraphs for better pacing
        content = topic['content']
        paragraphs = content.split('. ')

        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                # Add period back if needed
                if not paragraph.endswith('.'):
                    paragraph += '.'

                speak_text(paragraph, speed=0.85)
                time.sleep(0.8)  # Pause between paragraphs

        time.sleep(1)

        # Provide next options
        options = """Tutorial complete.

You can say:
- 'Repeat tutorial' to hear it again
- 'Back to topics' to select another topic
- 'Quiz me' to test your understanding
- 'Next topic' to continue to the next topic"""

        speak_text(options, speed=0.9)

        return {
            'success': True,
            'message': 'Tutorial delivered',
            'topic': topic['title'],
            'action': 'tutorial_complete'
        }

    def repeat_current_content(self) -> Dict[str, Any]:
        """Repeat current tutorial or menu"""
        if self.menu_level == 'content' and self.current_topic:
            return self.start_tutorial(self.current_topic)
        elif self.menu_level == 'topic' and self.available_topics:
            self._present_topic_menu(self.available_topics)
            return {'success': True, 'action': 'menu_repeated'}
        elif self.menu_level == 'subject':
            return self.list_available_subjects()
        else:
            message = "Nothing to repeat. Say 'Help' for commands."
            speak_text(message)
            return {'success': False, 'message': message}

    def go_back(self) -> Dict[str, Any]:
        """Navigate back to previous menu level"""
        play_beep(800, 150)

        if self.menu_level == 'content':
            self.menu_level = 'topic'
            self.current_topic = None
            self._present_topic_menu(self.available_topics)
            return {'success': True, 'action': 'back_to_topics'}

        elif self.menu_level == 'topic':
            self.menu_level = 'subject'
            self.current_subject = None
            self.available_topics = []
            return self.list_available_subjects()

        elif self.menu_level == 'subject':
            self.menu_level = 'main'
            speak_text("Returning to main menu. Say 'Help' for available commands.")
            return {'success': True, 'action': 'back_to_main'}

        else:
            speak_text("Already at main menu.")
            return {'success': False, 'message': 'At main menu'}

    def provide_help(self) -> str:
        """Provide comprehensive help for VI students"""
        play_ready_signal()

        help_message = """AIVI Voice Commands Help:

NAVIGATION COMMANDS:
- 'List subjects' - Hear all available subjects
- 'Learn' plus subject name - Start learning a subject
- 'Select' plus number - Choose a menu option
- 'Repeat' - Repeat current content or menu
- 'Back' - Go to previous menu
- 'Help' - Hear this help message

LEARNING COMMANDS:
- 'Repeat tutorial' - Hear the tutorial again
- 'Next topic' - Move to next topic
- 'Quiz me' - Test your knowledge
- 'Explain more' - Get detailed explanation

DOCUMENT COMMANDS:
- 'Read my notes' - Read uploaded documents
- 'Summarize document' - Get document summary

GENERAL COMMANDS:
- 'Search' plus query - Search for information
- 'Stop listening' - Stop voice mode
- 'Exit' - Close the application

Say any command clearly after the beep sound."""

        speak_text(help_message, speed=0.85)
        return help_message

    def search_and_present(self, query: str) -> Dict[str, Any]:
        """Search offline data and present results with voice"""
        play_ready_signal()

        speak_text(f"Searching for: {query}", speed=0.9)

        results = self.offline_data.search_offline_data(query)

        if not results:
            message = f"I couldn't find any information about '{query}' in the offline database. Would you like me to search online? Say 'Yes' or 'No'."
            speak_text(message)
            play_beep(400, 300)
            return {
                'success': False,
                'message': message,
                'query': query,
                'prompt_online_search': True
            }

        # Present best result
        best_result = results[0]

        announcement = f"I found {len(results)} results. Here is the best match:"
        speak_text(announcement, speed=0.9)
        time.sleep(0.5)

        speak_text(f"Question: {best_result['question']}", speed=0.9)
        time.sleep(0.5)

        speak_text(f"Answer: {best_result['answer']}", speed=0.85)

        if len(results) > 1:
            time.sleep(1)
            prompt = f"I have {len(results) - 1} more results. Say 'More results' to hear them, or 'Back' to return."
            speak_text(prompt, speed=0.9)

        play_success_beep()

        return {
            'success': True,
            'message': 'Search completed',
            'query': query,
            'results': results,
            'action': 'search_complete'
        }

    def get_current_state(self) -> Dict[str, Any]:
        """Get current learning session state"""
        return {
            'menu_level': self.menu_level,
            'current_subject': self.current_subject,
            'current_topic': self.current_topic['title'] if self.current_topic else None,
            'available_subjects_count': len(self.available_subjects),
            'available_topics_count': len(self.available_topics)
        }
