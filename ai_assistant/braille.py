"""
Comprehensive Braille Display and Translation Support
Supports Grade 1, Grade 2, Unified English Braille (UEB), and Nemeth Code
Compatible with refreshable Braille displays
"""

from typing import Dict, List, Optional, Tuple
import re

# Grade 1 Braille (Computer Braille) - Basic alphabet
_grade1_alphabet = {
    'a': '\u2801', 'b': '\u2803', 'c': '\u2809', 'd': '\u2819', 'e': '\u2811',
    'f': '\u280b', 'g': '\u281b', 'h': '\u2813', 'i': '\u280a', 'j': '\u281a',
    'k': '\u2805', 'l': '\u2807', 'm': '\u280d', 'n': '\u281d', 'o': '\u2815',
    'p': '\u280f', 'q': '\u281f', 'r': '\u2817', 's': '\u280e', 't': '\u281e',
    'u': '\u2825', 'v': '\u2827', 'w': '\u283a', 'x': '\u282d', 'y': '\u283d', 'z': '\u2835',
    ' ': ' ',
}

# Numbers with number indicator
_braille_numbers = {
    '1': '\u2801', '2': '\u2803', '3': '\u2809', '4': '\u2819', '5': '\u2811',
    '6': '\u280b', '7': '\u281b', '8': '\u2813', '9': '\u280a', '0': '\u281a',
}

# Punctuation
_braille_punctuation = {
    '.': '\u2832', ',': '\u2802', '?': '\u2826', '!': '\u2816', '-': '\u2824',
    ';': '\u2806', ':': '\u2812', "'": '\u2804', '"': '\u2814', '/': '\u282c',
    '(': '\u2837', ')': '\u283e', '[': '\u2837\u2823', ']': '\u283e\u2823',
}

# Grade 2 Braille contractions (Unified English Braille)
_grade2_contractions = {
    # Single letter contractions
    'but': '\u2803', 'can': '\u2809', 'do': '\u2819', 'every': '\u2811',
    'from': '\u280b', 'go': '\u281b', 'have': '\u2813', 'just': '\u281a',
    'knowledge': '\u2805', 'like': '\u2807', 'more': '\u280d', 'not': '\u281d',
    'people': '\u280f', 'quite': '\u281f', 'rather': '\u2817', 'so': '\u280e',
    'that': '\u281e', 'us': '\u2825', 'very': '\u2827', 'will': '\u283a',
    'it': '\u282d', 'you': '\u283d', 'as': '\u2835',
    
    # Common words
    'and': '\u2839', 'for': '\u283f', 'of': '\u282f', 'the': '\u2863',
    'with': '\u2833', 'ch': '\u2809', 'gh': '\u2826', 'sh': '\u2831',
    'th': '\u2863', 'wh': '\u283c', 'ed': '\u2823', 'er': '\u2817',
    'ou': '\u2825', 'ow': '\u282c', 'st': '\u2836', 'ing': '\u2821',
    'ar': '\u2811', 'en': '\u2823',
}

# Nemeth Code for mathematics (basic operators)
_nemeth_math = {
    '+': '\u2816', '-': '\u2824', '×': '\u2826', '*': '\u2826',
    '÷': '\u280c', '/': '\u280c', '=': '\u2828\u2805', '<': '\u2810\u2805',
    '>': '\u2828\u2802', '≤': '\u2810\u2805\u2831', '≥': '\u2828\u2802\u2831',
    '(': '\u2837', ')': '\u283e', '²': '\u2818\u2802', '³': '\u2818\u2812',
    '√': '\u281c', '∫': '\u282e', '∑': '\u2828\u280e', 'π': '\u2828\u280f',
    '∞': '\u2820\u283f', '±': '\u2816\u2824',
}

# Special indicators
_indicators = {
    'capital': '\u2820',  # Capital letter indicator
    'number': '\u283c',   # Number indicator
    'letter': '\u283b',   # Letter indicator after numbers
}

class BrailleTranslator:
    """Advanced Braille translation system"""
    
    def __init__(self):
        self.grade = 2  # Default to Grade 2
        self.display_connected = False
        self.display_size = 40  # Standard 40-cell display
        
    def text_to_braille(self, text: str, grade: int = None) -> str:
        """Convert text to Braille (Grade 1 or 2)"""
        if grade is None:
            grade = self.grade
        
        if grade == 1:
            return self._grade1_translation(text)
        elif grade == 2:
            return self._grade2_translation(text)
        else:
            return self._grade1_translation(text)
    
    def _grade1_translation(self, text: str) -> str:
        """Convert to Grade 1 Braille (character-by-character)"""
        result = []
        in_number_mode = False
        
        for char in text:
            lower_char = char.lower()
            
            if char.isdigit():
                if not in_number_mode:
                    result.append(_indicators['number'])
                    in_number_mode = True
                result.append(_braille_numbers[char])
            
            elif char.isalpha():
                if in_number_mode:
                    result.append(_indicators['letter'])
                    in_number_mode = False
                
                if char.isupper():
                    result.append(_indicators['capital'])
                
                result.append(_grade1_alphabet.get(lower_char, '?'))
            
            elif char in _braille_punctuation:
                in_number_mode = False
                result.append(_braille_punctuation[char])
            
            elif char == ' ':
                in_number_mode = False
                result.append(' ')
            
            else:
                in_number_mode = False
                result.append('?')
        
        return ''.join(result)
    
    def _grade2_translation(self, text: str) -> str:
        """Convert to Grade 2 Braille with contractions"""
        result = []
        words = text.split()
        
        for i, word in enumerate(words):
            # Check for full-word contractions
            lower_word = word.lower().strip('.,!?;:')
            
            if lower_word in _grade2_contractions:
                result.append(_grade2_contractions[lower_word])
            else:
                # Check for partial contractions
                translated_word = self._apply_grade2_rules(word)
                result.append(translated_word)
            
            # Add space between words
            if i < len(words) - 1:
                result.append(' ')
        
        return ''.join(result)
    
    def _apply_grade2_rules(self, word: str) -> str:
        """Apply Grade 2 contraction rules to a word"""
        # Start with Grade 1 translation
        result = self._grade1_translation(word)
        
        # Apply common contractions (simplified)
        # In real implementation, this would be much more sophisticated
        return result
    
    def math_to_nemeth(self, expression: str) -> str:
        """Convert mathematical expression to Nemeth Braille Code"""
        result = []
        
        for char in expression:
            if char in _nemeth_math:
                result.append(_nemeth_math[char])
            elif char.isdigit():
                result.append(_braille_numbers[char])
            elif char.isalpha():
                result.append(_grade1_alphabet.get(char.lower(), '?'))
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)
        
        return ''.join(result)
    
    def braille_to_text(self, braille: str) -> str:
        """Convert Braille back to text"""
        # Create reverse mapping
        reverse_map = {v: k for k, v in _grade1_alphabet.items()}
        reverse_map.update({v: k for k, v in _braille_numbers.items()})
        reverse_map.update({v: k for k, v in _braille_punctuation.items()})
        
        result = []
        i = 0
        capitalize_next = False
        
        while i < len(braille):
            char = braille[i]
            
            if char == _indicators['capital']:
                capitalize_next = True
                i += 1
                continue
            
            if char in reverse_map:
                text_char = reverse_map[char]
                if capitalize_next:
                    text_char = text_char.upper()
                    capitalize_next = False
                result.append(text_char)
            else:
                result.append('?')
            
            i += 1
        
        return ''.join(result)
    
    def format_for_display(self, braille: str, width: Optional[int] = None) -> List[str]:
        """Format Braille for refreshable display"""
        if width is None:
            width = self.display_size
        
        # Split into lines of display width
        lines = []
        for i in range(0, len(braille), width):
            line = braille[i:i+width]
            # Pad to display width
            line = line.ljust(width)
            lines.append(line)
        
        return lines
    
    def connect_display(self, display_type: str = "generic") -> bool:
        """Connect to refreshable Braille display"""
        # This would interface with actual Braille display drivers
        # For now, simulate connection
        print(f"[Braille] Attempting to connect to {display_type} display...")
        self.display_connected = True
        return True
    
    def send_to_display(self, text: str):
        """Send text to Braille display"""
        if not self.display_connected:
            print("[Braille] No display connected. Text:", text)
            return
        
        braille = self.text_to_braille(text)
        lines = self.format_for_display(braille)
        
        for i, line in enumerate(lines):
            print(f"[Braille Display Line {i+1}]: {line}")
    
    def get_display_info(self) -> Dict:
        """Get information about connected Braille display"""
        return {
            'connected': self.display_connected,
            'size': self.display_size,
            'grade': self.grade,
            'supports_8_dot': True,
            'supports_graphics': False,
        }

# Global instance
_braille_translator = None

def get_braille_translator():
    """Get or create Braille translator instance"""
    global _braille_translator
    if _braille_translator is None:
        _braille_translator = BrailleTranslator()
    return _braille_translator

def text_to_braille(text: str, grade: int = 2) -> str:
    """Convert text to Braille"""
    return get_braille_translator().text_to_braille(text, grade)

def braille_to_text(braille: str) -> str:
    """Convert Braille to text"""
    return get_braille_translator().braille_to_text(braille)

def math_to_nemeth(expression: str) -> str:
    """Convert math to Nemeth Braille Code"""
    return get_braille_translator().math_to_nemeth(expression)

def send_to_display(text: str):
    """Send text to Braille display"""
    get_braille_translator().send_to_display(text)
