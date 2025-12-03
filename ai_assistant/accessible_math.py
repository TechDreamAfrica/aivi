"""
Accessible Mathematics System for Visually Impaired Students
Supports LaTeX to speech, MathML, Nemeth Braille, audio graphing
"""

import re
import math
from typing import Dict, List, Tuple, Optional
import ai_assistant.tts as tts

class AccessibleMath:
    """Converts mathematical expressions to accessible formats"""
    
    def __init__(self):
        self.nemeth_map = self._init_nemeth_code()
        
    def _init_nemeth_code(self) -> Dict[str, str]:
        """Initialize Nemeth Braille Code mappings"""
        return {
            '+': '⠖',  # plus
            '-': '⠤',  # minus
            '×': '⠦',  # times
            '*': '⠦',  # times
            '÷': '⠌',  # divided by
            '/': '⠌',  # divided by
            '=': '⠨⠅',  # equals
            '<': '⠐⠅',  # less than
            '>': '⠨⠂',  # greater than
            '≤': '⠐⠅⠱',  # less than or equal
            '≥': '⠨⠂⠱',  # greater than or equal
            '≠': '⠌⠨⠅',  # not equal
            '²': '⠘⠆',  # squared
            '³': '⠘⠒',  # cubed
            '√': '⠜',  # square root
            '∫': '⠮',  # integral
            '∑': '⠨⠎',  # summation
            'π': '⠨⠏',  # pi
            '∞': '⠠⠿',  # infinity
            'θ': '⠨⠹',  # theta
            '±': '⠖⠤',  # plus-minus
        }
    
    def latex_to_speech(self, latex: str) -> str:
        """Convert LaTeX mathematical expression to natural speech"""
        speech = latex
        
        # Fractions
        speech = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', 
                       lambda m: f"the fraction {m.group(1)} over {m.group(2)}", 
                       speech)
        
        # Square root
        speech = re.sub(r'\\sqrt\{([^}]+)\}', 
                       lambda m: f"square root of {m.group(1)}", 
                       speech)
        
        # Nth root
        speech = re.sub(r'\\sqrt\[([^]]+)\]\{([^}]+)\}', 
                       lambda m: f"{m.group(1)} root of {m.group(2)}", 
                       speech)
        
        # Exponents
        speech = re.sub(r'\^(\d+)', lambda m: f" raised to the power of {m.group(1)}", speech)
        speech = re.sub(r'\^\{([^}]+)\}', lambda m: f" raised to the power of {m.group(1)}", speech)
        
        # Subscripts
        speech = re.sub(r'_(\d+)', lambda m: f" sub {m.group(1)}", speech)
        speech = re.sub(r'_\{([^}]+)\}', lambda m: f" sub {m.group(1)}", speech)
        
        # Integrals
        speech = re.sub(r'\\int_\{([^}]+)\}\^\{([^}]+)\}', 
                       lambda m: f"integral from {m.group(1)} to {m.group(2)} of", 
                       speech)
        speech = re.sub(r'\\int', 'integral of', speech)
        
        # Summation
        speech = re.sub(r'\\sum_\{([^}]+)\}\^\{([^}]+)\}', 
                       lambda m: f"sum from {m.group(1)} to {m.group(2)} of", 
                       speech)
        speech = re.sub(r'\\sum', 'sum of', speech)
        
        # Limits
        speech = re.sub(r'\\lim_\{([^}]+)\\to([^}]+)\}', 
                       lambda m: f"limit as {m.group(1)} approaches {m.group(2)} of", 
                       speech)
        
        # Derivatives
        speech = re.sub(r'\\frac\{d\}\{d([^}]+)\}', lambda m: f"derivative with respect to {m.group(1)} of", speech)
        speech = speech.replace('\\partial', 'partial derivative')
        
        # Greek letters
        greek = {
            'alpha': 'alpha', 'beta': 'beta', 'gamma': 'gamma', 'delta': 'delta',
            'epsilon': 'epsilon', 'theta': 'theta', 'lambda': 'lambda', 'mu': 'mu',
            'pi': 'pi', 'sigma': 'sigma', 'tau': 'tau', 'phi': 'phi', 'omega': 'omega'
        }
        for letter, name in greek.items():
            speech = speech.replace(f'\\{letter}', name)
        
        # Mathematical operators
        speech = speech.replace('\\times', 'times')
        speech = speech.replace('\\cdot', 'dot')
        speech = speech.replace('\\div', 'divided by')
        speech = speech.replace('\\pm', 'plus or minus')
        speech = speech.replace('\\leq', 'less than or equal to')
        speech = speech.replace('\\geq', 'greater than or equal to')
        speech = speech.replace('\\neq', 'not equal to')
        speech = speech.replace('\\approx', 'approximately equal to')
        speech = speech.replace('\\equiv', 'equivalent to')
        speech = speech.replace('\\infty', 'infinity')
        
        # Parentheses
        speech = speech.replace('\\left(', 'open parenthesis')
        speech = speech.replace('\\right)', 'close parenthesis')
        speech = speech.replace('\\left[', 'open bracket')
        speech = speech.replace('\\right]', 'close bracket')
        speech = speech.replace('\\left\\{', 'open brace')
        speech = speech.replace('\\right\\}', 'close brace')
        
        # Clean up remaining LaTeX commands
        speech = re.sub(r'\\[a-zA-Z]+', '', speech)
        speech = re.sub(r'[{}]', '', speech)
        
        return speech.strip()
    
    def to_nemeth_braille(self, expression: str) -> str:
        """Convert mathematical expression to Nemeth Braille Code"""
        result = []
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            # Check for multi-character operators
            if i < len(expression) - 1:
                two_char = expression[i:i+2]
                if two_char in self.nemeth_map:
                    result.append(self.nemeth_map[two_char])
                    i += 2
                    continue
            
            # Single character
            if char in self.nemeth_map:
                result.append(self.nemeth_map[char])
            elif char.isdigit():
                result.append(self._number_to_nemeth(char))
            elif char.isalpha():
                result.append(self._letter_to_nemeth(char))
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    def _number_to_nemeth(self, digit: str) -> str:
        """Convert digit to Nemeth Braille number"""
        nemeth_numbers = {
            '0': '⠴', '1': '⠂', '2': '⠆', '3': '⠒', '4': '⠲',
            '5': '⠢', '6': '⠖', '7': '⠶', '8': '⠦', '9': '⠔'
        }
        return nemeth_numbers.get(digit, digit)
    
    def _letter_to_nemeth(self, letter: str) -> str:
        """Convert letter to Nemeth Braille"""
        # Simplified - in real implementation, use full Braille alphabet
        return letter.lower()
    
    def describe_equation(self, equation: str, step_by_step: bool = True) -> List[str]:
        """Provide audio description of equation solving steps"""
        steps = []
        
        # Identify equation type
        if '=' in equation:
            left, right = equation.split('=', 1)
            steps.append(f"We have an equation: {self.latex_to_speech(left)} equals {self.latex_to_speech(right)}")
            
            # Check for linear equation
            if 'x' in equation and '^' not in equation and '²' not in equation:
                steps.extend(self._solve_linear(left.strip(), right.strip()))
            # Check for quadratic
            elif '²' in equation or '^2' in equation:
                steps.append("This is a quadratic equation. We can solve it using the quadratic formula.")
                steps.append("The quadratic formula is: x equals negative b plus or minus square root of b squared minus 4 a c, all divided by 2 a")
        
        return steps
    
    def _solve_linear(self, left: str, right: str) -> List[str]:
        """Solve and describe linear equation steps"""
        steps = []
        steps.append("To solve this linear equation:")
        steps.append("Step 1: Collect all terms with x on the left side")
        steps.append("Step 2: Collect all constant terms on the right side")
        steps.append("Step 3: Divide both sides by the coefficient of x")
        steps.append("Step 4: Simplify to find x")
        return steps
    
    def audio_graph_description(self, function: str, x_range: Tuple[float, float], 
                                points: int = 20) -> List[str]:
        """Generate audio description of mathematical function graph"""
        descriptions = []
        x_min, x_max = x_range
        step = (x_max - x_min) / points
        
        descriptions.append(f"Graphing function: {self.latex_to_speech(function)}")
        descriptions.append(f"X range from {x_min} to {x_max}")
        
        # Evaluate function at key points
        try:
            # Simple evaluation for basic functions
            prev_y = None
            for i in range(points):
                x = x_min + i * step
                # This is simplified - real implementation would parse and evaluate properly
                if 'x^2' in function or 'x²' in function:
                    y = x ** 2
                elif 'x^3' in function:
                    y = x ** 3
                elif 'sin' in function:
                    y = math.sin(x)
                elif 'cos' in function:
                    y = math.cos(x)
                else:
                    y = x  # Linear default
                
                if prev_y is not None:
                    if y > prev_y:
                        trend = "increasing"
                    elif y < prev_y:
                        trend = "decreasing"
                    else:
                        trend = "constant"
                    
                    if i % 5 == 0:  # Report every 5th point
                        descriptions.append(f"At x = {x:.2f}, y = {y:.2f}, function is {trend}")
                
                prev_y = y
        
        except Exception as e:
            descriptions.append(f"Unable to evaluate function: {str(e)}")
        
        return descriptions
    
    def sonify_data(self, data: List[float], duration_seconds: float = 2.0) -> str:
        """Convert numerical data to audio tones (sonification)"""
        # This would generate audio tones corresponding to data values
        # For now, return description
        if not data:
            return "No data to sonify"
        
        min_val = min(data)
        max_val = max(data)
        
        description = f"Data sonification: {len(data)} data points ranging from {min_val:.2f} to {max_val:.2f}. "
        
        # Describe trend
        if len(data) > 1:
            increasing = sum(1 for i in range(1, len(data)) if data[i] > data[i-1])
            decreasing = sum(1 for i in range(1, len(data)) if data[i] < data[i-1])
            
            if increasing > decreasing:
                description += "Overall increasing trend. Higher pitches indicate larger values."
            elif decreasing > increasing:
                description += "Overall decreasing trend. Lower pitches indicate smaller values."
            else:
                description += "Fluctuating trend with no clear direction."
        
        return description
    
    def matrix_to_speech(self, matrix: List[List[float]]) -> str:
        """Convert matrix to audio description"""
        if not matrix:
            return "Empty matrix"
        
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        
        description = f"Matrix with {rows} rows and {cols} columns. "
        
        for i, row in enumerate(matrix):
            description += f"Row {i+1}: "
            for j, val in enumerate(row):
                description += f"Column {j+1} is {val}, "
            description += ". "
        
        return description
    
    def speak_math(self, expression: str, format: str = 'latex'):
        """Speak mathematical expression using TTS"""
        if format == 'latex':
            speech = self.latex_to_speech(expression)
        else:
            speech = expression
        
        tts.speak_text(speech)
        return speech

# Global instance
_accessible_math = None

def get_accessible_math():
    """Get or create accessible math instance"""
    global _accessible_math
    if _accessible_math is None:
        _accessible_math = AccessibleMath()
    return _accessible_math

def latex_to_speech(latex: str) -> str:
    """Convert LaTeX to speech"""
    return get_accessible_math().latex_to_speech(latex)

def to_nemeth_braille(expression: str) -> str:
    """Convert to Nemeth Braille"""
    return get_accessible_math().to_nemeth_braille(expression)

def describe_equation(equation: str) -> List[str]:
    """Get step-by-step equation description"""
    return get_accessible_math().describe_equation(equation)

def audio_graph(function: str, x_range: Tuple[float, float] = (-10, 10)) -> List[str]:
    """Get audio graph description"""
    return get_accessible_math().audio_graph_description(function, x_range)
