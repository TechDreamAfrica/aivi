"""
Conversation Memory System
Stores, retrieves, and learns from conversation history
"""

import json
import os
from datetime import datetime
from pathlib import Path
import pickle

class ConversationMemory:
    def __init__(self, user_id="default_user"):
        self.user_id = user_id
        self.memory_dir = Path("user_data") / user_id
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.conversations_file = self.memory_dir / "conversations.json"
        self.user_profile_file = self.memory_dir / "profile.json"
        self.learning_data_file = self.memory_dir / "learning_data.pkl"
        
        self.current_session = []
        self.user_profile = self.load_user_profile()
        self.learning_data = self.load_learning_data()
        
    def load_user_profile(self):
        """Load user profile with preferences and characteristics"""
        if self.user_profile_file.exists():
            with open(self.user_profile_file, 'r') as f:
                return json.load(f)
        
        # Default profile
        return {
            'name': None,
            'created_at': datetime.now().isoformat(),
            'total_conversations': 0,
            'total_messages': 0,
            'favorite_topics': [],
            'difficulty_level': 'intermediate',
            'learning_style': 'unknown',  # visual, auditory, kinesthetic
            'common_questions': [],
            'interaction_patterns': {},
            'accessibility_needs': [],
            'last_active': datetime.now().isoformat()
        }
    
    def save_user_profile(self):
        """Save user profile to disk"""
        self.user_profile['last_active'] = datetime.now().isoformat()
        with open(self.user_profile_file, 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def load_learning_data(self):
        """Load machine learning data for personalization"""
        if self.learning_data_file.exists():
            with open(self.learning_data_file, 'rb') as f:
                return pickle.load(f)
        
        return {
            'topic_frequency': {},
            'question_types': {},
            'success_patterns': [],
            'difficulty_adjustments': {},
            'response_preferences': {}
        }
    
    def save_learning_data(self):
        """Save learning data for ML"""
        with open(self.learning_data_file, 'wb') as f:
            pickle.dump(self.learning_data, f)
    
    def add_message(self, role, content, metadata=None):
        """Add a message to current session"""
        message = {
            'role': role,  # 'user' or 'assistant'
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.current_session.append(message)
        
        # Update statistics
        self.user_profile['total_messages'] += 1
        
        # Analyze message for learning
        if role == 'user':
            self._analyze_user_message(content, metadata)
        
        return message
    
    def _analyze_user_message(self, content, metadata):
        """Analyze user message to learn patterns"""
        # Extract topics
        content_lower = content.lower()
        
        # Track topic frequency
        topics = self._extract_topics(content_lower)
        for topic in topics:
            self.learning_data['topic_frequency'][topic] = \
                self.learning_data['topic_frequency'].get(topic, 0) + 1
        
        # Track question types
        question_type = self._classify_question(content_lower)
        self.learning_data['question_types'][question_type] = \
            self.learning_data['question_types'].get(question_type, 0) + 1
        
        # Update user preferences
        if metadata:
            if 'satisfaction' in metadata:
                self._update_success_patterns(content, metadata['satisfaction'])
    
    def _extract_topics(self, text):
        """Extract topics from text"""
        topic_keywords = {
            'math': ['math', 'calculate', 'equation', 'algebra', 'geometry'],
            'science': ['science', 'physics', 'chemistry', 'biology'],
            'english': ['english', 'grammar', 'writing', 'literature'],
            'history': ['history', 'historical', 'ancient', 'modern'],
            'programming': ['code', 'programming', 'python', 'javascript'],
            'general': ['question', 'help', 'explain', 'what', 'how']
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ['general']
    
    def _classify_question(self, text):
        """Classify type of question"""
        if any(word in text for word in ['what', 'define', 'meaning']):
            return 'definition'
        elif any(word in text for word in ['how', 'steps', 'process']):
            return 'explanation'
        elif any(word in text for word in ['why', 'reason', 'because']):
            return 'reasoning'
        elif any(word in text for word in ['solve', 'calculate', 'find']):
            return 'problem_solving'
        elif any(word in text for word in ['example', 'show me', 'demonstrate']):
            return 'example_request'
        else:
            return 'general'
    
    def _update_success_patterns(self, content, satisfaction):
        """Update patterns based on user satisfaction"""
        pattern = {
            'content': content[:100],  # First 100 chars
            'satisfaction': satisfaction,
            'timestamp': datetime.now().isoformat()
        }
        self.learning_data['success_patterns'].append(pattern)
        
        # Keep only last 100 patterns
        if len(self.learning_data['success_patterns']) > 100:
            self.learning_data['success_patterns'] = \
                self.learning_data['success_patterns'][-100:]
    
    def save_session(self):
        """Save current session to conversation history"""
        if not self.current_session:
            return
        
        session_data = {
            'session_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'start_time': self.current_session[0]['timestamp'],
            'end_time': self.current_session[-1]['timestamp'],
            'message_count': len(self.current_session),
            'messages': self.current_session
        }
        
        # Load existing conversations
        conversations = []
        if self.conversations_file.exists():
            with open(self.conversations_file, 'r') as f:
                conversations = json.load(f)
        
        conversations.append(session_data)
        
        # Save updated conversations
        with open(self.conversations_file, 'w') as f:
            json.dump(conversations, f, indent=2)
        
        # Update profile statistics
        self.user_profile['total_conversations'] += 1
        self.save_user_profile()
        self.save_learning_data()
        
        # Clear current session
        self.current_session = []
        
        return session_data
    
    def get_recent_conversations(self, n=5):
        """Get recent n conversations"""
        if not self.conversations_file.exists():
            return []
        
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        
        return conversations[-n:] if conversations else []
    
    def search_conversations(self, query):
        """Search through conversation history"""
        if not self.conversations_file.exists():
            return []
        
        with open(self.conversations_file, 'r') as f:
            conversations = json.load(f)
        
        query_lower = query.lower()
        results = []
        
        for conv in conversations:
            for msg in conv['messages']:
                if query_lower in msg['content'].lower():
                    results.append({
                        'session_id': conv['session_id'],
                        'timestamp': msg['timestamp'],
                        'role': msg['role'],
                        'content': msg['content']
                    })
        
        return results
    
    def get_context_for_query(self, query, n_recent=3):
        """Get relevant context from past conversations"""
        recent = self.get_recent_conversations(n_recent)
        search_results = self.search_conversations(query)
        
        context = {
            'recent_topics': self._get_recent_topics(recent),
            'related_discussions': search_results[:3],
            'user_expertise_level': self._estimate_expertise_level(query),
            'preferred_response_style': self.user_profile.get('learning_style', 'unknown')
        }
        
        return context
    
    def _get_recent_topics(self, conversations):
        """Extract topics from recent conversations"""
        topics = []
        for conv in conversations:
            for msg in conv.get('messages', []):
                if msg['role'] == 'user':
                    topics.extend(self._extract_topics(msg['content'].lower()))
        
        # Count frequency
        from collections import Counter
        topic_counts = Counter(topics)
        return topic_counts.most_common(5)
    
    def _estimate_expertise_level(self, query):
        """Estimate user's expertise level for a topic"""
        topics = self._extract_topics(query.lower())
        
        if not topics:
            return 'beginner'
        
        # Check frequency of topic discussions
        total_queries = sum(
            self.learning_data['topic_frequency'].get(topic, 0)
            for topic in topics
        )
        
        if total_queries > 50:
            return 'advanced'
        elif total_queries > 20:
            return 'intermediate'
        else:
            return 'beginner'
    
    def get_personalized_greeting(self):
        """Generate personalized greeting based on user data"""
        name = self.user_profile.get('name')
        total_convs = self.user_profile.get('total_conversations', 0)
        
        if name:
            greeting = f"Welcome back, {name}!"
        else:
            greeting = "Hello!"
        
        if total_convs > 0:
            greeting += f" We've had {total_convs} conversations together. How can I help you today?"
        else:
            greeting += " I'm AIVI, your AI learning assistant. What would you like to learn today?"
        
        return greeting
    
    def get_statistics(self):
        """Get user statistics"""
        return {
            'total_conversations': self.user_profile['total_conversations'],
            'total_messages': self.user_profile['total_messages'],
            'member_since': self.user_profile['created_at'],
            'favorite_topics': self._get_top_topics(5),
            'most_asked_questions': self._get_common_question_types(),
            'learning_progress': self._calculate_learning_progress()
        }
    
    def _get_top_topics(self, n=5):
        """Get top n topics by frequency"""
        from collections import Counter
        topic_freq = Counter(self.learning_data['topic_frequency'])
        return topic_freq.most_common(n)
    
    def _get_common_question_types(self):
        """Get most common question types"""
        from collections import Counter
        question_types = Counter(self.learning_data['question_types'])
        return question_types.most_common(3)
    
    def _calculate_learning_progress(self):
        """Calculate learning progress metrics"""
        total_queries = self.user_profile['total_messages'] // 2  # Approximate user messages
        
        if total_queries < 10:
            return 'just_started'
        elif total_queries < 50:
            return 'building_knowledge'
        elif total_queries < 200:
            return 'progressing_well'
        else:
            return 'advanced_learner'
    
    def update_user_name(self, name):
        """Update user's name"""
        self.user_profile['name'] = name
        self.save_user_profile()
    
    def update_learning_style(self, style):
        """Update user's learning style preference"""
        if style in ['visual', 'auditory', 'kinesthetic', 'mixed']:
            self.user_profile['learning_style'] = style
            self.save_user_profile()
    
    def add_accessibility_need(self, need):
        """Add accessibility requirement"""
        if need not in self.user_profile['accessibility_needs']:
            self.user_profile['accessibility_needs'].append(need)
            self.save_user_profile()
    
    def export_data(self, export_dir=None):
        """Export all user data"""
        if not export_dir:
            export_dir = Path("exports") / self.user_id
        export_dir = Path(export_dir)
        export_dir.mkdir(parents=True, exist_ok=True)
        
        # Export conversations
        if self.conversations_file.exists():
            import shutil
            shutil.copy(self.conversations_file, export_dir / "conversations.json")
        
        # Export profile
        with open(export_dir / "profile.json", 'w') as f:
            json.dump(self.user_profile, f, indent=2)
        
        # Export statistics
        stats = self.get_statistics()
        with open(export_dir / "statistics.json", 'w') as f:
            json.dump(stats, f, indent=2)
        
        return export_dir

# Global instance
_memory_instance = None

def get_memory(user_id="default_user"):
    """Get or create conversation memory instance"""
    global _memory_instance
    if _memory_instance is None or _memory_instance.user_id != user_id:
        _memory_instance = ConversationMemory(user_id)
    return _memory_instance

def add_user_message(content, metadata=None):
    """Add user message to memory"""
    memory = get_memory()
    return memory.add_message('user', content, metadata)

def add_assistant_message(content, metadata=None):
    """Add assistant message to memory"""
    memory = get_memory()
    return memory.add_message('assistant', content, metadata)

def save_current_session():
    """Save current conversation session"""
    memory = get_memory()
    return memory.save_session()

def get_conversation_context(query):
    """Get relevant context for a query"""
    memory = get_memory()
    return memory.get_context_for_query(query)

def get_user_stats():
    """Get user statistics"""
    memory = get_memory()
    return memory.get_statistics()
