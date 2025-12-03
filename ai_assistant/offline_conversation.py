"""
Enhanced Offline AI Conversation System
Provides natural language conversation using offline academic data
with context awareness and memory
"""

import re
import random
import json
import os
from datetime import datetime
from . import offline_academic
from . import tts

# Try to import Ollama integration
try:
    from . import ollama_integration
    OLLAMA_AVAILABLE = True
except ImportError:
    ollama_integration = None
    OLLAMA_AVAILABLE = False

class OfflineConversationAI:
    def __init__(self):
        self.conversation_history = []
        self.user_context = {
            'name': None,
            'preferences': {},
            'current_topic': None,
            'session_start': datetime.now(),
            'questions_asked': 0,
            'topics_discussed': []
        }
        self.personality_traits = {
            'helpful': 0.9,
            'encouraging': 0.8,
            'patient': 0.9,
            'knowledgeable': 0.85,
            'empathetic': 0.8
        }

        # Check Ollama availability at initialization
        self.ollama_ready = False
        if OLLAMA_AVAILABLE:
            try:
                status = ollama_integration.get_ollama_status()
                self.ollama_ready = status.get("ready_for_offline", False)
                if self.ollama_ready:
                    print("[Conversation AI] Ollama available for enhanced responses")
                else:
                    print("[Conversation AI] Ollama not ready, using fallback responses")
            except Exception as e:
                print(f"[Conversation AI] Error checking Ollama: {e}")
                self.ollama_ready = False
        
    def process_conversation(self, user_input, context=None):
        """
        Process user input and generate contextual response
        """
        user_input = user_input.strip()
        if not user_input:
            return "I'm here to help. What would you like to know or discuss?"
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'context': context
        })
        
        # Analyze user input
        intent = self._analyze_intent(user_input)
        response = self._generate_response(user_input, intent, context)
        
        # Add response to history
        self.conversation_history[-1]['ai_response'] = response
        
        # Update user context
        self._update_context(user_input, intent)
        
        return response
    
    def _analyze_intent(self, user_input):
        """
        Analyze user intent from input
        """
        input_lower = user_input.lower()
        
        intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'question': ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'can you explain'],
            'help_request': ['help', 'assist', 'support', 'guide', 'show me', 'teach me'],
            'academic_query': ['explain', 'define', 'meaning of', 'tell me about', 'what is', 'how does'],
            'math_problem': ['solve', 'calculate', 'formula', 'equation', 'math', 'mathematics'],
            'study_help': ['study', 'learn', 'practice', 'quiz', 'test', 'exam', 'homework'],
            'personal': ['I am', 'my name is', 'I like', 'I prefer', 'I need', 'I want'],
            'gratitude': ['thank', 'thanks', 'appreciate', 'grateful'],
            'goodbye': ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit'],
            'emotional': ['frustrated', 'confused', 'worried', 'happy', 'excited', 'sad', 'angry'],
            'clarification': ['repeat', 'again', 'clarify', 'explain again', 'I don\'t understand'],
            'encouragement_needed': ['difficult', 'hard', 'struggling', 'can\'t understand', 'give up']
        }
        
        detected_intents = []
        for intent, keywords in intents.items():
            if any(keyword in input_lower for keyword in keywords):
                detected_intents.append(intent)
        
        # Return primary intent (first detected) or 'general' if none found
        return detected_intents[0] if detected_intents else 'general'
    
    def _generate_response(self, user_input, intent, context=None):
        """
        Generate appropriate response based on intent and context
        """
        # Handle different intents
        if intent == 'greeting':
            return self._handle_greeting(user_input)
        elif intent == 'question' or intent == 'academic_query':
            return self._handle_academic_question(user_input)
        elif intent == 'help_request':
            return self._handle_help_request(user_input)
        elif intent == 'math_problem':
            return self._handle_math_problem(user_input)
        elif intent == 'study_help':
            return self._handle_study_help(user_input)
        elif intent == 'personal':
            return self._handle_personal_info(user_input)
        elif intent == 'gratitude':
            return self._handle_gratitude()
        elif intent == 'goodbye':
            return self._handle_goodbye()
        elif intent == 'emotional':
            return self._handle_emotional_support(user_input)
        elif intent == 'clarification':
            return self._handle_clarification_request()
        elif intent == 'encouragement_needed':
            return self._handle_encouragement()
        else:
            return self._handle_general_query(user_input)
    
    def _handle_greeting(self, user_input):
        """Handle greeting messages"""
        greetings = [
            "Hello! I'm AIVI, your AI assistant. How can I help you today?",
            "Hi there! I'm here to help with your studies and questions. What would you like to know?",
            "Good to see you! I'm ready to assist with academics, accessibility, or any questions you have.",
            "Hello! Welcome to AIVI. I can help with studies, answer questions, and assist with accessibility needs."
        ]
        
        greeting = random.choice(greetings)
        
        # Personalize if we know the user's name
        if self.user_context['name']:
            greeting = greeting.replace("Hello!", f"Hello {self.user_context['name']}!")
            greeting = greeting.replace("Hi there!", f"Hi {self.user_context['name']}!")
        
        return greeting
    
    def _handle_academic_question(self, user_input):
        """Handle academic questions using offline data"""
        # Extract key terms from the question
        question_words = ['what', 'how', 'when', 'where', 'why', 'who', 'which', 'define', 'explain']
        
        # Remove question words to get the core topic
        words = user_input.lower().split()
        content_words = [word for word in words if word not in question_words and len(word) > 2]
        
        # Search for academic content
        search_terms = ' '.join(content_words)
        academic_response = offline_academic.offline_search(search_terms)
        
        if "No information found" in academic_response:
            # Try individual words if combined search fails
            for word in content_words:
                academic_response = offline_academic.offline_search(word)
                if "No information found" not in academic_response:
                    break
        
        # Enhance the response with conversational elements
        if "No information found" in academic_response:
            response = f"I don't have specific information about '{search_terms}' in my offline database. "
            response += "However, I can help you with other academic topics like mathematics, English, science, or history. "
            response += "What specific subject area interests you?"
        else:
            response = f"Great question! {academic_response}"
            response += "\n\nWould you like me to explain anything further or do you have related questions?"
        
        # Update current topic
        self.user_context['current_topic'] = search_terms
        self.user_context['questions_asked'] += 1
        
        return response
    
    def _handle_help_request(self, user_input):
        """Handle general help requests"""
        help_responses = [
            "I'm here to help! I can assist with academic questions, accessibility features, study planning, and more. What specific area do you need help with?",
            "Of course! I can help with studying, answering questions, reading text, converting to Braille, solving math problems, and many other tasks. What would you like to do?",
            "I'd be happy to help! I have access to academic information in math, science, English, and history. I can also help with accessibility needs. What interests you?",
            "Absolutely! I'm designed to help with education and accessibility. I can explain concepts, help with homework, read text aloud, and much more. How can I assist you today?"
        ]
        
        return random.choice(help_responses)
    
    def _handle_math_problem(self, user_input):
        """Handle math-related queries"""
        # Try to extract mathematical content
        if any(op in user_input for op in ['+', '-', '*', '/', '=', 'plus', 'minus', 'times', 'divided']):
            response = "I can help with math problems! For complex calculations, you might want to use the math solver feature. "
            response += "Could you state the problem clearly? For example: 'solve 2 plus 3' or 'what is 15 divided by 3'?"
        else:
            # Search for math topics in offline data
            math_response = offline_academic.offline_search(user_input)
            if "No information found" not in math_response:
                response = f"Here's what I know about that: {math_response}"
            else:
                response = "I can help with various math topics including arithmetic, algebra, geometry, and more. "
                response += "What specific math concept would you like to learn about?"
        
        return response
    
    def _handle_study_help(self, user_input):
        """Handle study-related requests"""
        study_tips = [
            "Great that you're focusing on studying! I can help you with specific subjects, create study schedules, or quiz you on topics. What subject are you working on?",
            "I'm here to support your studies! I can explain concepts, help with homework, or create practice questions. What would be most helpful right now?",
            "Study time is important! I can assist with understanding difficult concepts, organizing your study schedule, or providing explanations. What's your current focus?",
            "Excellent! Learning is a journey. I can help break down complex topics, provide examples, or quiz you. What subject or topic are you studying?"
        ]
        
        response = random.choice(study_tips)
        
        # Add encouragement based on personality
        if self.personality_traits['encouraging'] > 0.7:
            encouragements = [
                " You're doing great by seeking help!",
                " Keep up the excellent work!",
                " I believe in your ability to learn this!",
                " Every question you ask helps you learn more!"
            ]
            response += random.choice(encouragements)
        
        return response
    
    def _handle_personal_info(self, user_input):
        """Handle personal information from user"""
        input_lower = user_input.lower()
        
        # Extract name if provided
        if 'my name is' in input_lower:
            name_part = input_lower.split('my name is')[1].strip()
            name = name_part.split()[0].capitalize() if name_part else None
            if name:
                self.user_context['name'] = name
                return f"Nice to meet you, {name}! I'm AIVI, and I'm here to help with your studies and accessibility needs. What would you like to work on today?"
        
        # Handle preferences
        if 'i like' in input_lower or 'i prefer' in input_lower:
            return "That's great to know! Understanding your preferences helps me assist you better. How can I help you today?"
        
        # Handle needs/wants
        if 'i need' in input_lower or 'i want' in input_lower:
            return "I understand. Let me know specifically what you need help with, and I'll do my best to assist you."
        
        return "Thank you for sharing that with me. How can I help you today?"
    
    def _handle_gratitude(self):
        """Handle thank you messages"""
        gratitude_responses = [
            "You're very welcome! I'm happy to help anytime.",
            "My pleasure! Feel free to ask if you have more questions.",
            "Glad I could help! Is there anything else you'd like to know?",
            "You're welcome! I'm here whenever you need assistance.",
            "Happy to help! Don't hesitate to ask if you need anything else."
        ]
        return random.choice(gratitude_responses)
    
    def _handle_goodbye(self):
        """Handle goodbye messages"""
        goodbyes = [
            "Goodbye! Feel free to come back anytime you need help with studies or have questions.",
            "See you later! Remember, I'm always here to help with your learning journey.",
            "Take care! Come back anytime you need academic assistance or have questions.",
            "Farewell! Good luck with your studies, and don't hesitate to return if you need help."
        ]
        
        goodbye = random.choice(goodbyes)
        
        if self.user_context['name']:
            goodbye = goodbye.replace("Goodbye!", f"Goodbye, {self.user_context['name']}!")
            goodbye = goodbye.replace("See you later!", f"See you later, {self.user_context['name']}!")
        
        return goodbye
    
    def _handle_emotional_support(self, user_input):
        """Handle emotional expressions and provide support"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['frustrated', 'confused', 'worried']):
            return "I understand this can be challenging. Take a deep breath - we'll work through this together. What specific part is giving you trouble?"
        
        elif any(word in input_lower for word in ['happy', 'excited']):
            return "That's wonderful! I'm glad you're feeling positive. How can I help you continue this great momentum?"
        
        elif any(word in input_lower for word in ['sad', 'angry']):
            return "I'm sorry you're feeling this way. Sometimes learning can be overwhelming, but remember that every expert was once a beginner. What can I do to help?"
        
        return "I'm here to support you through your learning journey. What would help you feel more confident right now?"
    
    def _handle_clarification_request(self):
        """Handle requests for clarification"""
        if self.conversation_history:
            last_response = self.conversation_history[-1].get('ai_response', '')
            return f"Let me explain that differently: {last_response}\n\nIs there a specific part you'd like me to clarify further?"
        
        return "I'd be happy to clarify! What specifically would you like me to explain in more detail?"
    
    def _handle_encouragement(self):
        """Provide encouragement when user is struggling"""
        encouragements = [
            "Don't give up! Learning takes time and practice. Every challenge you overcome makes you stronger. What specific part can we work on together?",
            "I believe in you! Sometimes concepts take time to click. Let's break this down into smaller, manageable pieces. What's the first thing you'd like to understand?",
            "You're not alone in finding this difficult - it means you're challenging yourself! That's how real learning happens. How can I help make this clearer?",
            "Remember, every expert was once confused too. Your persistence is admirable! Let's tackle this step by step. What would help most right now?"
        ]
        return random.choice(encouragements)
    
    def _handle_general_query(self, user_input):
        """Handle general queries that don't fit specific categories"""
        # Try to search offline academic data
        academic_response = offline_academic.offline_search(user_input)
        
        if "No information found" not in academic_response:
            return f"I found this information: {academic_response}\n\nWould you like me to explain anything further?"
        
        # Provide general helpful response
        general_responses = [
            "I'm not sure I fully understand. Could you rephrase your question or be more specific about what you'd like to know?",
            "That's an interesting question! Could you provide more details so I can help you better?",
            "I want to make sure I give you the best answer. Could you tell me more about what you're looking for?",
            "I'm here to help! Could you clarify what specific information or assistance you need?"
        ]
        
        return random.choice(general_responses)
    
    def _update_context(self, user_input, intent):
        """Update user context based on conversation"""
        input_lower = user_input.lower()
        
        # Track topics discussed
        if intent == 'academic_query':
            topic = self.user_context.get('current_topic')
            if topic and topic not in self.user_context['topics_discussed']:
                self.user_context['topics_discussed'].append(topic)
        
        # Update preferences based on repeated queries
        if intent in self.user_context['preferences']:
            self.user_context['preferences'][intent] += 1
        else:
            self.user_context['preferences'][intent] = 1
    
    def get_conversation_summary(self):
        """Get a summary of the current conversation session"""
        total_exchanges = len(self.conversation_history)
        session_duration = datetime.now() - self.user_context['session_start']
        
        summary = {
            'session_duration_minutes': session_duration.total_seconds() / 60,
            'total_exchanges': total_exchanges,
            'questions_asked': self.user_context['questions_asked'],
            'topics_discussed': self.user_context['topics_discussed'],
            'most_common_intent': max(self.user_context['preferences'], key=self.user_context['preferences'].get) if self.user_context['preferences'] else None
        }
        
        return summary
    
    def save_conversation_history(self, filename=None):
        """Save conversation history to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aivi_conversation_{timestamp}.json"
        
        data = {
            'conversation_history': [
                {
                    'timestamp': item['timestamp'].isoformat(),
                    'user': item['user'],
                    'ai_response': item.get('ai_response', ''),
                    'context': item.get('context', {})
                }
                for item in self.conversation_history
            ],
            'user_context': {
                **self.user_context,
                'session_start': self.user_context['session_start'].isoformat()
            },
            'summary': self.get_conversation_summary()
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"Conversation saved to {filename}"
        except Exception as e:
            return f"Failed to save conversation: {str(e)}"

# Global conversation AI instance
conversation_ai = OfflineConversationAI()

def chat_with_ai(message, context=None):
    """Main function to chat with the offline AI"""
    return conversation_ai.process_conversation(message, context)

def get_conversation_stats():
    """Get conversation statistics"""
    return conversation_ai.get_conversation_summary()

def save_session():
    """Save current conversation session"""
    return conversation_ai.save_conversation_history()
