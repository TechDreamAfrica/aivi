"""
Mathematics and Formula Reader module
"""
from .offline_academic import get_mode, set_mode
import math
import os
import ast
import operator

# Load environment variables from .env file (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, environment variables won't be loaded from .env file
    pass

def safe_eval_math(expression, allowed_names):
    """
    Safely evaluate mathematical expressions without using eval()
    Uses AST parsing to prevent code injection attacks
    """
    # Supported operators for mathematical expressions
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    def eval_node(node):
        if isinstance(node, ast.Num):  # Numbers (deprecated in Python 3.8+)
            return node.n
        elif isinstance(node, ast.Constant):  # Numbers in Python 3.8+
            return node.value
        elif isinstance(node, ast.Name):  # Variables/functions
            if node.id in allowed_names:
                return allowed_names[node.id]
            else:
                raise ValueError(f"Name '{node.id}' is not allowed")
        elif isinstance(node, ast.BinOp):  # Binary operations
            left = eval_node(node.left)
            right = eval_node(node.right)
            op = operators.get(type(node.op))
            if op:
                return op(left, right)
            else:
                raise ValueError(f"Operator {type(node.op).__name__} not supported")
        elif isinstance(node, ast.UnaryOp):  # Unary operations
            operand = eval_node(node.operand)
            op = operators.get(type(node.op))
            if op:
                return op(operand)
            else:
                raise ValueError(f"Unary operator {type(node.op).__name__} not supported")
        elif isinstance(node, ast.Call):  # Function calls
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name and func_name in allowed_names:
                func = allowed_names[func_name]
                args = [eval_node(arg) for arg in node.args]
                return func(*args)
            else:
                raise ValueError(f"Function '{func_name}' is not allowed")
        else:
            raise ValueError(f"Node type {type(node).__name__} not supported")
    
    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode='eval')
        return eval_node(tree.body)
    except SyntaxError as e:
        raise ValueError(f"Invalid mathematical expression: {e}")
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {e}")

def preprocess_math_expression(problem):
    """Enhanced preprocessing for natural language math expressions"""
    # Convert common math terms to Python syntax
    replacements = {
        # Basic operations
        ' plus ': '+', ' add ': '+', ' and ': '+',
        ' minus ': '-', ' subtract ': '-', ' less ': '-', ' take away ': '-',
        ' times ': '*', ' multiply ': '*', ' multiplied by ': '*', ' of ': '*',
        ' divided by ': '/', ' divide ': '/', ' over ': '/', ' per ': '/',
        ' to the power of ': '**', ' raised to ': '**', '^': '**', ' to the ': '**',
        ' squared': '**2', ' cubed': '**3', ' to the fourth': '**4', ' to the fifth': '**5',
        
        # Common symbols and alternatives
        'x': '*', 'X': '*', '÷': '/', '×': '*', '·': '*',
        ' mod ': '%', ' modulo ': '%', ' remainder ': '%',
        
        # Numbers in words (extended)
        ' zero ': '0', ' one ': '1', ' two ': '2', ' three ': '3',
        ' four ': '4', ' five ': '5', ' six ': '6', ' seven ': '7',
        ' eight ': '8', ' nine ': '9', ' ten ': '10', ' eleven ': '11',
        ' twelve ': '12', ' thirteen ': '13', ' fourteen ': '14', ' fifteen ': '15',
        ' sixteen ': '16', ' seventeen ': '17', ' eighteen ': '18', ' nineteen ': '19',
        ' twenty ': '20', ' thirty ': '30', ' forty ': '40', ' fifty ': '50',
        ' sixty ': '60', ' seventy ': '70', ' eighty ': '80', ' ninety ': '90',
        ' hundred ': '100', ' thousand ': '1000',
        
        # Mathematical functions (extended)
        ' square root of ': 'sqrt(', ' sqrt ': 'sqrt(', ' root ': 'sqrt(',
        ' absolute value of ': 'abs(', ' abs ': 'abs(',
        ' sine of ': 'sin(', ' sin ': 'sin(', ' cosine of ': 'cos(', ' cos ': 'cos(',
        ' tangent of ': 'tan(', ' tan ': 'tan(',
        ' log ': 'log(', ' ln ': 'log(', ' logarithm of ': 'log(',
        ' natural log of ': 'log(', ' log base 10 of ': 'log10(',
        ' exponential ': 'exp(', ' exp ': 'exp(',
        
        # Constants
        ' pi ': 'pi', ' PI ': 'pi', ' euler ': 'e', ' eulers number ': 'e',
        
        # Percentage
        ' percent': '/100', '%': '/100',
        
        # Common phrases
        ' what is ': '', ' calculate ': '', ' solve ': '', ' find ': '',
        ' equals ': '=', ' equal to ': '=', ' is ': '=',
        
        # Clean up multiple spaces
        '  ': ' ', '   ': ' '
    }
    
    processed = problem.lower().strip()
    
    # Remove question words at the beginning
    question_starters = ['what is', 'how much is', 'calculate', 'solve', 'find']
    for starter in question_starters:
        if processed.startswith(starter):
            processed = processed[len(starter):].strip()
    
    # Apply replacements
    for old, new in replacements.items():
        processed = processed.replace(old, new)
    
    # Handle parentheses for functions
    functions_needing_close = ['sqrt(', 'abs(', 'sin(', 'cos(', 'tan(', 'log(', 'log10(', 'exp(']
    for func in functions_needing_close:
        if func in processed and processed.count('(') > processed.count(')'):
            # Find the end of the function argument
            func_pos = processed.find(func)
            if func_pos != -1:
                # Look for the next operator or end of string
                search_start = func_pos + len(func)
                operators = ['+', '-', '*', '/', ')', '=', ' ']
                next_op_pos = len(processed)
                for op in operators:
                    op_pos = processed.find(op, search_start)
                    if op_pos != -1 and op_pos < next_op_pos:
                        next_op_pos = op_pos
                
                # Insert closing parenthesis
                if next_op_pos < len(processed):
                    processed = processed[:next_op_pos] + ')' + processed[next_op_pos:]
                else:
                    processed += ')'
    
    # Handle equations (convert = to a solvable format for simple cases)
    if '=' in processed and not any(op in processed for op in ['solve', 'factor', 'expand']):
        parts = processed.split('=')
        if len(parts) == 2:
            left, right = parts[0].strip(), parts[1].strip()
            # For simple linear equations like "x + 5 = 10"
            if 'x' in left and right.replace('.', '').replace('-', '').isdigit():
                # This is a basic equation - we'll handle it differently
                processed = f"solve({left} - ({right}))"
    
    return processed

def read_formula(formula):
    # Describe a math formula in plain English using simple rules
    print(f"[Math] Reading formula: {formula}")
    # For demo, just repeat the formula. For real use, integrate with MathPix or LaTeX parser.
    return f"The formula is: {formula}"

def solve_math_problem(problem, gui_callback=None):
    """
    Solve math problem using WolframAlpha if online, else use Python math module
    gui_callback: optional callback function for GUI integration
    """
    print(f"[Math] Solving: {problem}")
    mode = get_mode() if callable(globals().get('get_mode', None)) else 'offline'
    
    if mode == 'offline':
        try:
            # Enhanced preprocessing for natural language math
            preprocessed = preprocess_math_expression(problem)
            print(f"[Math] Preprocessed: {preprocessed}")
            
            # Handle special cases
            if 'solve(' in preprocessed:
                return solve_simple_equation(preprocessed, problem)
            
            # Only allow safe math expressions
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            allowed_names.update({
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sum': sum, 'pow': pow, 'divmod': divmod
            })
            
            # Use safe_eval instead of eval for security
            result = safe_eval_math(preprocessed, allowed_names)
            
            # Format the result nicely
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 6)  # Round to 6 decimal places
            
            # Create detailed response
            response = f"Solution: {result}"
            if gui_callback:
                response += f"\n\nSteps:\n1. Original: {problem}\n2. Processed: {preprocessed}\n3. Result: {result}"
            
            return response
            
        except Exception as e:
            error_msg = f"Could not solve offline: {str(e)}"
            print(f"[Math] {error_msg}")
            
            # Try to provide helpful suggestions
            suggestions = get_math_suggestions(problem)
            
            # For GUI integration, return a helpful message instead of prompting
            if gui_callback:
                return f"Unable to solve '{problem}' offline.\n\n{suggestions}\n\nTry switching to online mode for advanced calculations."
            
            # Speak the error (TTS integration point)
            try:
                from .tts import speak_text
                speak_text(f"Sorry, could not solve the problem offline. {str(e)}")
            except Exception:
                pass
            
            return f"Unable to solve '{problem}' offline.\n\n{suggestions}"
    else:
        return solve_online_math(problem)

def solve_simple_equation(preprocessed, original_problem):
    """Solve simple linear equations offline"""
    try:
        # Extract the equation from solve(expression)
        if preprocessed.startswith('solve(') and preprocessed.endswith(')'):
            equation = preprocessed[6:-1]  # Remove 'solve(' and ')'
            
            # For simple linear equations like "x + 5 - 10"
            # This is a basic solver - in practice you'd want a more sophisticated one
            if 'x' in equation:
                # Try to solve for x by rearranging
                # This is a simplified approach
                return f"This appears to be an equation with variable 'x'.\nFor complex equations, please use online mode.\n\nEquation: {original_problem}"
        
        return "Equation solving requires online mode for accurate results."
    except Exception as e:
        return f"Error solving equation: {str(e)}"

def solve_online_math(problem):
    """Solve math using WolframAlpha online"""
    try:
        import wolframalpha
        app_id = os.getenv("WOLFRAMALPHA_APP_ID")
        if not app_id:
            return "WolframAlpha App ID not set. Please configure WOLFRAMALPHA_APP_ID environment variable for online math solving."
        
        client = wolframalpha.Client(app_id)
        res = client.query(problem)
        
        # Check if there are any results
        if hasattr(res, 'results') and res.results is not None:
            try:
                answer = next(res.results).text
                return f"Solution: {answer}"
            except StopIteration:
                print("[Math] No answer found from WolframAlpha.")
                return "Sorry, no answer found for this problem. Please try rephrasing or simplifying your question."
        else:
            print("[Math] No results attribute in WolframAlpha response.")
            return "Sorry, no answer found for this problem. Please try rephrasing or simplifying your question."
            
    except Exception as e:
        error_msg = f"Online calculation error: {str(e)}"
        print(f"[Math] {error_msg}")
        # Speak the error (TTS integration point)
        try:
            from .tts import speak_text
            speak_text(f"Sorry, could not solve the problem online. {str(e)}")
        except Exception:
            pass
        return f"Unable to solve '{problem}' online. Error: {str(e)}\n\nPlease check your internet connection or try simplifying the problem."

# Helper functions for enhanced math solver
def get_math_examples():
    """Return categorized math examples for the GUI"""
    return {
        "Basic Arithmetic": [
            "2 + 3 * 4",
            "sqrt(25) + 10",
            "15 / 3 - 2",
            "2^3 + 4^2",
            "15 divided by 3",
            "square root of 16",
            "2 to the power of 8"
        ],
        "Algebra": [
            "solve x + 5 = 15",
            "solve 2x - 3 = 7",
            "x^2 + 5x + 6",
            "factor x^2 - 4",
            "solve x + 5 = 10",
            "factor x^2 + 5x + 6",
            "expand (x + 2)(x + 3)"
        ],
        "Trigonometry": [
            "sin(30)",
            "cos(pi/4)",
            "tan(45 degrees)",
            "asin(0.5)",
            "sin(30 degrees)",
            "cos(pi/4)",
            "tan(45 degrees)"
        ],
        "Natural Language": [
            "what is the square root of sixteen",
            "two plus three times four",
            "solve for x when x plus five equals fifteen",
            "what is sin of thirty degrees"
        ],
        "Calculus": [
            "derivative of x^2 + 3x + 1",
            "integral of 2x + 1",
            "limit of (x^2 - 1)/(x - 1) as x approaches 1"
        ]
    }

def get_math_suggestions(problem):
    """Get helpful suggestions based on the problem type"""
    suggestions = "Suggestions:\n"
    
    if any(word in problem.lower() for word in ['solve', 'equation', '=']):
        suggestions += "• For equations, try online mode\n"
        suggestions += "• Simplify to basic arithmetic if possible\n"
    
    if any(func in problem.lower() for func in ['derivative', 'integral', 'limit']):
        suggestions += "• Calculus requires online mode\n"
        suggestions += "• Try basic algebra instead\n"
    
    if any(word in problem.lower() for word in ['factor', 'expand', 'polynomial']):
        suggestions += "• Algebraic manipulation requires online mode\n"
        suggestions += "• Try numerical calculations\n"
    
    suggestions += "• Use basic operations: +, -, *, /, **, sqrt()\n"
    suggestions += "• Example: '2 + 3 * 4' or 'sqrt(16)'"
    
    return suggestions


def format_math_result(result, problem):
    """Format math result for better display"""
    if result.startswith("Solution:"):
        return result
    
    # Add some formatting for better readability
    formatted = f"Problem: {problem}\n"
    formatted += f"Answer: {result}\n"
    
    # Add explanation if it's a simple calculation
    try:
        if any(op in problem for op in ['+', '-', '*', '/']):
            formatted += f"\nThis is a basic arithmetic calculation."
    except Exception as e:
        print(f"Warning: Error formatting math result: {e}")
        pass
    
    return formatted
