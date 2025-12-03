"""
Offline Manager - Comprehensive offline data management and functionality
Handles CSV data storage, user input collection, and offline capabilities
"""

import os
import csv
import json
import logging
import sqlite3
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
import pickle

class OfflineDataManager:
    def __init__(self, data_dir: str = "offline_data"):
        """Initialize offline data manager"""
        self.data_dir = data_dir
        self.csv_file = os.path.join(data_dir, "aivi_knowledge_base.csv")
        self.db_file = os.path.join(data_dir, "aivi_data.db")
        self.user_interactions_file = os.path.join(data_dir, "user_interactions.csv")
        self.search_cache_file = os.path.join(data_dir, "search_cache.csv")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Initialize data structures
        self._initialize_data_files()
        self._initialize_database()
        
        self.logger.info("Offline Data Manager initialized")

    def _initialize_data_files(self):
        """Initialize CSV data files if they don't exist"""
        # Knowledge base CSV
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'category', 'question', 'answer', 'keywords', 'source', 'timestamp', 'confidence'])
                
                # Add some initial data
                initial_data = [
                    ['1', 'general', 'What is AI?', 'Artificial Intelligence (AI) is technology that enables machines to simulate human intelligence...', 'ai,artificial intelligence,machine learning', 'builtin', datetime.now().isoformat(), '0.9'],
                    ['2', 'academic', 'What is photosynthesis?', 'Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce glucose and oxygen...', 'photosynthesis,plants,biology', 'builtin', datetime.now().isoformat(), '0.95'],
                    ['3', 'science', 'What is gravity?', 'Gravity is a fundamental force that attracts objects with mass toward each other...', 'gravity,physics,force', 'builtin', datetime.now().isoformat(), '0.9'],
                ]
                writer.writerows(initial_data)
        
        # User interactions CSV
        if not os.path.exists(self.user_interactions_file):
            with open(self.user_interactions_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'user_input', 'response', 'response_type', 'satisfaction', 'keywords'])
        
        # Search cache CSV
        if not os.path.exists(self.search_cache_file):
            with open(self.search_cache_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['query_hash', 'query', 'response', 'source', 'timestamp', 'access_count'])

    def _initialize_database(self):
        """Initialize SQLite database for advanced queries"""
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    question TEXT,
                    answer TEXT,
                    keywords TEXT,
                    source TEXT,
                    timestamp TEXT,
                    confidence REAL,
                    access_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    response TEXT,
                    rating INTEGER,
                    feedback TEXT,
                    timestamp TEXT
                )
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_keywords ON knowledge_base(keywords)
            ''')
            
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_category ON knowledge_base(category)
            ''')

    def search_offline_data(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search offline knowledge base"""
        with self._lock:
            try:
                results = []
                query_lower = query.lower()
                
                # Search CSV data
                with open(self.csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Check if query matches question, answer, or keywords
                        if (query_lower in row['question'].lower() or 
                            query_lower in row['answer'].lower() or 
                            any(keyword.strip().lower() in query_lower for keyword in row['keywords'].split(','))):
                            
                            if category is None or row['category'].lower() == category.lower():
                                result = {
                                    'id': row['id'],
                                    'category': row['category'],
                                    'question': row['question'],
                                    'answer': row['answer'],
                                    'keywords': row['keywords'],
                                    'source': row['source'],
                                    'confidence': float(row['confidence']),
                                    'relevance_score': self._calculate_relevance(query_lower, row)
                                }
                                results.append(result)
                
                # Sort by relevance score
                results.sort(key=lambda x: x['relevance_score'], reverse=True)
                
                # Update access count for top results
                for result in results[:3]:
                    self._update_access_count(result['id'])
                
                return results[:10]  # Return top 10 results
                
            except Exception as e:
                self.logger.error(f"Error searching offline data: {e}")
                return []

    def _calculate_relevance(self, query: str, row: Dict[str, str]) -> float:
        """Calculate relevance score for a search result"""
        score = 0.0
        
        # Exact matches in question get highest score
        if query in row['question'].lower():
            score += 1.0
        
        # Partial matches in question
        query_words = query.split()
        question_words = row['question'].lower().split()
        common_words = set(query_words) & set(question_words)
        score += len(common_words) / len(query_words) * 0.8
        
        # Keyword matches
        keywords = [k.strip().lower() for k in row['keywords'].split(',')]
        for word in query_words:
            if word in keywords:
                score += 0.6
        
        # Answer relevance
        if query in row['answer'].lower():
            score += 0.4
        
        # Confidence factor
        score *= float(row['confidence'])
        
        return score

    def _update_access_count(self, record_id: str):
        """Update access count for a knowledge base entry"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute(
                    "UPDATE knowledge_base SET access_count = access_count + 1 WHERE id = ?",
                    (record_id,)
                )
        except Exception as e:
            self.logger.error(f"Error updating access count: {e}")

    def add_knowledge_entry(self, category: str, question: str, answer: str, 
                          keywords: List[str], source: str = "user", confidence: float = 0.8):
        """Add new knowledge entry to offline database"""
        with self._lock:
            try:
                # Add to CSV
                with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    entry_id = self._generate_id()
                    writer.writerow([
                        entry_id, category, question, answer, 
                        ','.join(keywords), source, datetime.now().isoformat(), confidence
                    ])
                
                # Add to database
                with sqlite3.connect(self.db_file) as conn:
                    conn.execute(
                        "INSERT INTO knowledge_base (category, question, answer, keywords, source, timestamp, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (category, question, answer, ','.join(keywords), source, datetime.now().isoformat(), confidence)
                    )
                
                self.logger.info(f"Added knowledge entry: {question[:50]}...")
                return True
                
            except Exception as e:
                self.logger.error(f"Error adding knowledge entry: {e}")
                return False
    
    def add_to_knowledge_base(self, category: str, question: str, answer: str,
                             source: str = "user", confidence: float = 0.8,
                             difficulty_level: str = "medium", academic_field: str = "General"):
        """
        Add entry to knowledge base with extended fields
        Wrapper for add_knowledge_entry with additional academic metadata
        """
        # Extract keywords from question and answer
        keywords = []
        import re
        words = re.findall(r'\b\w+\b', question.lower() + ' ' + answer.lower())
        # Get unique, meaningful words (longer than 3 chars)
        keywords = list(set([w for w in words if len(w) > 3]))[:10]
        
        return self.add_knowledge_entry(category, question, answer, keywords, source, confidence)

    def record_user_interaction(self, user_input: str, response: str, 
                              response_type: str, satisfaction: int = None, keywords: List[str] = None):
        """Record user interaction for learning"""
        with self._lock:
            try:
                with open(self.user_interactions_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().isoformat(),
                        user_input,
                        response,
                        response_type,
                        satisfaction or '',
                        ','.join(keywords) if keywords else ''
                    ])
                
                self.logger.info("Recorded user interaction")
                return True
                
            except Exception as e:
                self.logger.error(f"Error recording user interaction: {e}")
                return False

    def cache_online_search(self, query: str, response: str, source: str = "online"):
        """Cache online search results for offline use"""
        with self._lock:
            try:
                query_hash = hashlib.md5(query.encode()).hexdigest()
                
                # Check if already cached
                cached = False
                updated_rows = []
                
                with open(self.search_cache_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['query_hash'] == query_hash:
                            row['access_count'] = str(int(row['access_count']) + 1)
                            row['timestamp'] = datetime.now().isoformat()
                            cached = True
                        updated_rows.append(row)
                
                if not cached:
                    # Add new cache entry
                    with open(self.search_cache_file, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([query_hash, query, response, source, datetime.now().isoformat(), 1])
                else:
                    # Update existing entry
                    with open(self.search_cache_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=['query_hash', 'query', 'response', 'source', 'timestamp', 'access_count'])
                        writer.writeheader()
                        writer.writerows(updated_rows)
                
                # Also add to main knowledge base if it's valuable
                self._extract_knowledge_from_cache(query, response, source)
                
                self.logger.info(f"Cached search result for: {query[:50]}...")
                return True
                
            except Exception as e:
                self.logger.error(f"Error caching search result: {e}")
                return False

    def _extract_knowledge_from_cache(self, query: str, response: str, source: str):
        """Extract valuable knowledge from cached searches"""
        try:
            # Simple heuristics to determine if this should be added to knowledge base
            if (len(response) > 100 and 
                any(word in query.lower() for word in ['what is', 'explain', 'how to', 'define']) and
                source in ['ai', 'wikipedia', 'academic']):
                
                # Extract keywords from query
                keywords = [word.strip() for word in query.lower().split() if len(word) > 3]
                
                # Determine category
                category = 'general'
                if any(word in query.lower() for word in ['math', 'physics', 'chemistry', 'biology']):
                    category = 'science'
                elif any(word in query.lower() for word in ['history', 'literature', 'art']):
                    category = 'humanities'
                elif any(word in query.lower() for word in ['programming', 'code', 'computer']):
                    category = 'technology'
                
                self.add_knowledge_entry(category, query, response, keywords, source, 0.7)
                
        except Exception as e:
            self.logger.error(f"Error extracting knowledge from cache: {e}")

    def get_search_cache(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached search result"""
        try:
            query_hash = hashlib.md5(query.encode()).hexdigest()
            
            with open(self.search_cache_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['query_hash'] == query_hash:
                        # Update access count
                        self._update_cache_access(query_hash)
                        return {
                            'query': row['query'],
                            'response': row['response'],
                            'source': row['source'],
                            'timestamp': row['timestamp'],
                            'access_count': int(row['access_count'])
                        }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving search cache: {e}")
            return None

    def _update_cache_access(self, query_hash: str):
        """Update cache access count"""
        try:
            updated_rows = []
            
            with open(self.search_cache_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['query_hash'] == query_hash:
                        row['access_count'] = str(int(row['access_count']) + 1)
                    updated_rows.append(row)
            
            with open(self.search_cache_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['query_hash', 'query', 'response', 'source', 'timestamp', 'access_count'])
                writer.writeheader()
                writer.writerows(updated_rows)
                
        except Exception as e:
            self.logger.error(f"Error updating cache access: {e}")

    def _generate_id(self) -> str:
        """Generate unique ID for new entries"""
        return str(int(time.time() * 1000))

    def get_statistics(self) -> Dict[str, Any]:
        """Get offline data statistics"""
        try:
            stats = {
                'knowledge_entries': 0,
                'user_interactions': 0,
                'cached_searches': 0,
                'categories': set(),
                'most_accessed': []
            }
            
            # Count knowledge entries
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    stats['knowledge_entries'] += 1
                    stats['categories'].add(row['category'])
            
            # Count user interactions
            with open(self.user_interactions_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                stats['user_interactions'] = sum(1 for _ in reader)
            
            # Count cached searches
            with open(self.search_cache_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                cache_data = list(reader)
                stats['cached_searches'] = len(cache_data)
                
                # Get most accessed
                sorted_cache = sorted(cache_data, key=lambda x: int(x['access_count']), reverse=True)
                stats['most_accessed'] = [{'query': row['query'], 'count': row['access_count']} 
                                        for row in sorted_cache[:5]]
            
            stats['categories'] = list(stats['categories'])
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {}

    def export_data(self, export_path: str) -> bool:
        """Export all offline data to a directory"""
        try:
            os.makedirs(export_path, exist_ok=True)
            
            # Copy CSV files
            import shutil
            shutil.copy2(self.csv_file, export_path)
            shutil.copy2(self.user_interactions_file, export_path)
            shutil.copy2(self.search_cache_file, export_path)
            
            # Export database
            shutil.copy2(self.db_file, export_path)
            
            # Create summary report
            stats = self.get_statistics()
            with open(os.path.join(export_path, 'data_summary.json'), 'w') as f:
                json.dump(stats, f, indent=2, default=str)
            
            self.logger.info(f"Data exported to {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {e}")
            return False

    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old cached data"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            
            # Clean search cache
            updated_rows = []
            with open(self.search_cache_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    timestamp = datetime.fromisoformat(row['timestamp']).timestamp()
                    if timestamp > cutoff_date or int(row['access_count']) > 5:
                        updated_rows.append(row)
            
            with open(self.search_cache_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['query_hash', 'query', 'response', 'source', 'timestamp', 'access_count'])
                writer.writeheader()
                writer.writerows(updated_rows)
            
            self.logger.info(f"Cleaned up data older than {days_old} days")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cleaning up data: {e}")
            return False