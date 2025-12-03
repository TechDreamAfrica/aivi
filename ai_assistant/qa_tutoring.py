"""
Interactive Q&A and Tutoring module
"""
import random
from .offline_academic import offline_search, offline_data, get_mode

def answer_question(question):
    """
    Answer a question using offline data if in offline mode, else return a placeholder for online mode.
    """
    print(f"[Q&A] Answering: {question}")
    mode = get_mode() if callable(globals().get('get_mode', None)) else 'offline'
    if mode == 'offline':
        # Check for tutor command with what/why/who/when/how
        lowered = question.lower().strip()
        tutor_starts = ["what is ", "why is ", "who is ", "when is ", "how is ",
                        "what are ", "why are ", "who are ", "when are ", "how are ",
                        "what ", "why ", "who ", "when ", "how "]
        for start in tutor_starts:
            if lowered.startswith(start):
                # Remove the question word and search for the rest
                q = lowered[len(start):].strip(' ?')
                if not q:
                    break
                result = offline_search(q)
                if result and result != "No offline data found for your query.":
                    return f"{start.capitalize()}{q}?\n{result}"
                else:
                    return f"Sorry, I could not find an answer for: {q}"
        # Fallback to normal search
        return offline_search(question)
    else:
        # Placeholder for online Q&A (e.g., OpenAI API)
        return "Online Q&A not implemented."

def quiz_mode(level=None, subject=None, num_questions=5):
    """
    Start a quiz/flashcard mode using offline data.
    Each question is based on a topic, and the answer is the content from offline data.
    User can specify level and subject, or get random questions.
    """
    print("[Q&A] Starting quiz mode...")
    import time
    try:
        from .tts import speak
    except Exception:
        speak = None
    try:
        from .voice_commands import listen
    except Exception:
        listen = None
    def beep():
        try:
            import winsound
            winsound.Beep(1000, 200)
        except Exception:
            if speak:
                speak("Beep")
    
    # Gather all possible questions as (level, subject, topic, content)
    questions = []
    for lvl, subjects in offline_data.items():
        if level and lvl != level:
            continue
        for subj, topics in subjects.items():
            if subject and subj != subject:
                continue
            if isinstance(topics, dict):
                for topic, content in topics.items():
                    questions.append((lvl, subj, topic, content))
    if not questions:
        if speak:
            speak("No questions found for the selected level or subject.")
        print("No questions found for the selected level/subject.")
        return
    random.shuffle(questions)
    score = 0
    for i, (lvl, subj, topic, answer) in enumerate(questions[:num_questions]):
        qtext = f"Question {i+1}: {lvl.title()} {subj.title()} - What is {topic}?"
        if speak:
            speak(qtext)
        print(f"Q{i+1}: [{lvl.title()} > {subj.title()}] What is '{topic}'?")
        # Short pause for clarity
        time.sleep(0.7)
        # Beep or prompt before listening
        if speak:
            speak("Please answer after the beep.")
        beep()
        # Always use voice input if available
        user_input = None
        if listen:
            try:
                user_input = listen(prompt="Your answer:")
            except Exception:
                user_input = None
        if not user_input:
            if speak:
                speak("Please say your answer after the beep, or type it if voice is unavailable.")
            user_input = input("Your answer: ")
        # Repeat user's answer before feedback
        if user_input and user_input.strip():
            print(f"You answered: {user_input}")
            if speak:
                speak(f"You answered: {user_input}")
        print(f"A: {answer}\n")
        if speak:
            speak(f"The correct answer is: {answer}")
        # Simple answer checking: check if user's answer is in the correct answer (case-insensitive, partial match)
        if user_input and user_input.strip():
            if user_input.strip().lower() in answer.lower():
                feedback = "Correct!"
            else:
                feedback = "Wrong."
        else:
            feedback = "No answer received."
        print(feedback)
        if speak:
            speak(feedback)
        # Short pause between questions
        time.sleep(1.2)
    if speak:
        speak("Quiz complete!")
    print("Quiz complete!")
