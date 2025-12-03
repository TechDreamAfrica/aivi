"""
Exam Preparation System for Visually Impaired Students
Quiz generation, practice exams, time management, accessible strategies
"""

import random
import json
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import ai_assistant.tts as tts

class ExamPrepSystem:
    """Comprehensive exam preparation and practice system"""
    
    def __init__(self):
        self.quizzes_dir = "exam_prep/quizzes"
        self.progress_dir = "exam_prep/progress"
        self.strategies_dir = "exam_prep/strategies"
        
        for directory in [self.quizzes_dir, self.progress_dir, self.strategies_dir]:
            os.makedirs(directory, exist_ok=True)
        
        self.question_types = ['multiple_choice', 'true_false', 'short_answer', 'essay']
        self.difficulty_levels = ['easy', 'medium', 'hard']
    
    def generate_quiz(self, subject: str, topic: str, num_questions: int = 10,
                     difficulty: str = 'medium', question_type: str = 'multiple_choice') -> Dict:
        """Generate practice quiz from course materials"""
        quiz = {
            'id': f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'subject': subject,
            'topic': topic,
            'difficulty': difficulty,
            'question_type': question_type,
            'questions': [],
            'created_at': datetime.now().isoformat(),
            'time_limit': num_questions * 2,  # 2 minutes per question
        }
        
        # Generate questions (simulated - would use AI/knowledge base in production)
        for i in range(num_questions):
            question = self._generate_question(subject, topic, i+1, difficulty, question_type)
            quiz['questions'].append(question)
        
        # Save quiz
        quiz_file = os.path.join(self.quizzes_dir, f"{quiz['id']}.json")
        with open(quiz_file, 'w', encoding='utf-8') as f:
            json.dump(quiz, f, indent=2)
        
        return quiz
    
    def _generate_question(self, subject: str, topic: str, number: int,
                          difficulty: str, q_type: str) -> Dict:
        """Generate a single question"""
        if q_type == 'multiple_choice':
            return {
                'number': number,
                'type': 'multiple_choice',
                'question': f"Sample {difficulty} question about {topic} in {subject}?",
                'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                'correct_answer': 'Option A',
                'explanation': 'Explanation of why Option A is correct.',
                'points': 1 if difficulty == 'easy' else 2 if difficulty == 'medium' else 3,
            }
        
        elif q_type == 'true_false':
            return {
                'number': number,
                'type': 'true_false',
                'question': f"Statement about {topic}: This is true.",
                'correct_answer': 'true',
                'explanation': 'Explanation of the answer.',
                'points': 1,
            }
        
        elif q_type == 'short_answer':
            return {
                'number': number,
                'type': 'short_answer',
                'question': f"Explain {topic} in {subject}.",
                'key_points': ['Point 1', 'Point 2', 'Point 3'],
                'sample_answer': 'Sample answer explaining the topic...',
                'points': 5,
            }
        
        elif q_type == 'essay':
            return {
                'number': number,
                'type': 'essay',
                'question': f"Discuss the significance of {topic} in {subject}.",
                'rubric': {
                    'thesis': 2,
                    'arguments': 3,
                    'evidence': 3,
                    'conclusion': 2,
                },
                'points': 10,
            }
    
    def conduct_quiz_audio(self, quiz: Dict) -> Dict:
        """Conduct quiz with audio interface"""
        tts.speak_text(f"Starting quiz on {quiz['topic']} in {quiz['subject']}")
        tts.speak_text(f"This quiz has {len(quiz['questions'])} questions")
        tts.speak_text(f"Time limit: {quiz['time_limit']} minutes")
        
        results = {
            'quiz_id': quiz['id'],
            'started_at': datetime.now().isoformat(),
            'answers': [],
            'score': 0,
            'total_possible': 0,
        }
        
        for i, question in enumerate(quiz['questions'], 1):
            tts.speak_text(f"Question {i} of {len(quiz['questions'])}")
            
            if question['type'] == 'multiple_choice':
                answer = self._ask_multiple_choice(question)
                results['answers'].append({
                    'question_number': i,
                    'answer': answer,
                    'correct': answer == question['correct_answer'],
                })
                
                if answer == question['correct_answer']:
                    results['score'] += question['points']
                    tts.speak_text("Correct!")
                else:
                    tts.speak_text(f"Incorrect. The correct answer was {question['correct_answer']}")
                
                tts.speak_text(f"Explanation: {question['explanation']}")
            
            results['total_possible'] += question['points']
        
        results['completed_at'] = datetime.now().isoformat()
        results['percentage'] = (results['score'] / results['total_possible']) * 100
        
        # Announce results
        tts.speak_text(f"Quiz completed! Score: {results['score']} out of {results['total_possible']}")
        tts.speak_text(f"Percentage: {results['percentage']:.1f}%")
        
        # Save results
        self._save_results(results)
        
        return results
    
    def _ask_multiple_choice(self, question: Dict) -> str:
        """Ask multiple choice question with audio"""
        tts.speak_text(question['question'])
        tts.speak_text("Options:")
        
        for i, option in enumerate(question['options'], 1):
            tts.speak_text(f"Option {i}: {option}")
        
        # In real implementation, would wait for voice/keyboard input
        # For now, return simulated answer
        return random.choice(question['options'])
    
    def _save_results(self, results: Dict):
        """Save quiz results for progress tracking"""
        results_file = os.path.join(
            self.progress_dir,
            f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
    
    def get_progress_report(self, subject: Optional[str] = None,
                           days: int = 30) -> Dict:
        """Generate progress report with audio summary"""
        # Load all results from past N days
        cutoff_date = datetime.now() - timedelta(days=days)
        all_results = []
        
        for filename in os.listdir(self.progress_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.progress_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                    
                    result_date = datetime.fromisoformat(result['started_at'])
                    if result_date >= cutoff_date:
                        if subject is None or result.get('subject') == subject:
                            all_results.append(result)
        
        # Calculate statistics
        if not all_results:
            return {'message': 'No quiz data available'}
        
        total_quizzes = len(all_results)
        avg_score = sum(r['percentage'] for r in all_results) / total_quizzes
        highest_score = max(r['percentage'] for r in all_results)
        lowest_score = min(r['percentage'] for r in all_results)
        
        # Identify weak areas
        weak_areas = []
        strong_areas = []
        
        report = {
            'period': f'Last {days} days',
            'total_quizzes': total_quizzes,
            'average_score': avg_score,
            'highest_score': highest_score,
            'lowest_score': lowest_score,
            'weak_areas': weak_areas,
            'strong_areas': strong_areas,
            'recommendation': self._get_recommendation(avg_score),
        }
        
        return report
    
    def _get_recommendation(self, avg_score: float) -> str:
        """Get study recommendation based on performance"""
        if avg_score >= 90:
            return "Excellent performance! Continue current study methods. Consider helping peers."
        elif avg_score >= 75:
            return "Good performance. Review weak areas and practice more difficult questions."
        elif avg_score >= 60:
            return "Adequate performance. Increase study time and focus on problem areas."
        else:
            return "Need improvement. Consider study groups, tutoring, or different study methods."
    
    def speak_progress_report(self, report: Dict):
        """Read progress report aloud"""
        if 'message' in report:
            tts.speak_text(report['message'])
            return
        
        tts.speak_text("Progress Report")
        tts.speak_text(f"Period: {report['period']}")
        tts.speak_text(f"Total quizzes taken: {report['total_quizzes']}")
        tts.speak_text(f"Average score: {report['average_score']:.1f} percent")
        tts.speak_text(f"Highest score: {report['highest_score']:.1f} percent")
        tts.speak_text(f"Lowest score: {report['lowest_score']:.1f} percent")
        tts.speak_text(f"Recommendation: {report['recommendation']}")
    
    def get_test_taking_strategies(self, test_type: str = 'multiple_choice') -> List[str]:
        """Provide accessible test-taking strategies"""
        strategies = {
            'multiple_choice': [
                "Listen carefully to each question before considering options.",
                "Eliminate obviously wrong answers first to narrow choices.",
                "Watch for absolute words like 'always' or 'never' - they're often incorrect.",
                "If unsure, make an educated guess rather than leaving blank.",
                "Use process of elimination systematically.",
                "Read all options before selecting an answer.",
            ],
            'essay': [
                "Create a brief audio outline before writing.",
                "Start with a clear thesis statement in introduction.",
                "Use one main idea per paragraph.",
                "Provide specific examples and evidence.",
                "Write a strong conclusion that summarizes key points.",
                "Leave time to review using screen reader or TTS.",
            ],
            'short_answer': [
                "Answer the specific question asked - don't add unnecessary information.",
                "Use key terminology from course materials.",
                "Be concise but complete.",
                "Use bullet points if appropriate and allowed.",
            ],
            'true_false': [
                "Read/listen to the entire statement carefully.",
                "A statement must be entirely true to be marked true.",
                "Watch for qualifying words like 'usually', 'sometimes', 'often'.",
            ],
            'general': [
                "Arrive early to set up assistive technology.",
                "Confirm accommodations (extended time, screen reader, etc.) are in place.",
                "Use time management - allocate time per question.",
                "Answer easier questions first, mark difficult ones for review.",
                "If using audio output, adjust speech rate for optimal comprehension.",
                "Take short breaks if extended time is available.",
                "Review answers if time permits using accessible tools.",
            ],
        }
        
        return strategies.get(test_type, strategies['general'])
    
    def speak_strategies(self, test_type: str = 'multiple_choice'):
        """Read test-taking strategies aloud"""
        strategies = self.get_test_taking_strategies(test_type)
        
        tts.speak_text(f"Test-taking strategies for {test_type.replace('_', ' ')} questions:")
        
        for i, strategy in enumerate(strategies, 1):
            tts.speak_text(f"Strategy {i}: {strategy}")
    
    def create_study_schedule(self, exam_date: str, subjects: List[str],
                             hours_per_day: int = 2) -> Dict:
        """Create accessible study schedule"""
        exam_datetime = datetime.fromisoformat(exam_date)
        days_until_exam = (exam_datetime - datetime.now()).days
        
        if days_until_exam < 1:
            return {'error': 'Exam date must be in the future'}
        
        total_study_hours = days_until_exam * hours_per_day
        hours_per_subject = total_study_hours / len(subjects)
        
        schedule = {
            'exam_date': exam_date,
            'days_until_exam': days_until_exam,
            'total_study_hours': total_study_hours,
            'hours_per_subject': hours_per_subject,
            'daily_plan': [],
        }
        
        # Create daily schedule
        current_date = datetime.now()
        for day in range(days_until_exam):
            study_date = current_date + timedelta(days=day)
            subject_index = day % len(subjects)
            
            schedule['daily_plan'].append({
                'date': study_date.strftime('%Y-%m-%d'),
                'day_name': study_date.strftime('%A'),
                'subject': subjects[subject_index],
                'hours': hours_per_day,
                'tasks': [
                    'Review course materials',
                    'Practice problems',
                    'Take practice quiz',
                ],
            })
        
        # Add review days before exam
        if days_until_exam > 3:
            for i in range(3):
                schedule['daily_plan'][-3+i]['tasks'] = [
                    'Comprehensive review',
                    'Practice full-length exam',
                    'Review weak areas',
                ]
        
        return schedule
    
    def speak_study_schedule(self, schedule: Dict):
        """Read study schedule aloud"""
        if 'error' in schedule:
            tts.speak_text(schedule['error'])
            return
        
        tts.speak_text(f"Study schedule for exam on {schedule['exam_date']}")
        tts.speak_text(f"Days until exam: {schedule['days_until_exam']}")
        tts.speak_text(f"Total study hours planned: {schedule['total_study_hours']}")
        
        tts.speak_text("Daily study plan:")
        for day in schedule['daily_plan']:
            tts.speak_text(f"{day['day_name']}, {day['date']}: Study {day['subject']} for {day['hours']} hours")
            tts.speak_text(f"Tasks: {', '.join(day['tasks'])}")

# Global instance
_exam_prep = None

def get_exam_prep():
    """Get or create exam prep system"""
    global _exam_prep
    if _exam_prep is None:
        _exam_prep = ExamPrepSystem()
    return _exam_prep

def generate_quiz(subject: str, topic: str, num_questions: int = 10) -> Dict:
    """Generate practice quiz"""
    return get_exam_prep().generate_quiz(subject, topic, num_questions)

def get_test_strategies(test_type: str = 'multiple_choice') -> List[str]:
    """Get test-taking strategies"""
    return get_exam_prep().get_test_taking_strategies(test_type)

def create_study_schedule(exam_date: str, subjects: List[str]) -> Dict:
    """Create study schedule"""
    return get_exam_prep().create_study_schedule(exam_date, subjects)
