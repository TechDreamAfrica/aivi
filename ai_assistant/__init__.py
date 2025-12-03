# ai_assistant/__init__.py
# This file makes ai_assistant a package and exposes specific functions

# Core modules that should always work
from .tts import (
    speak_text,
    set_voice_mode,
    get_voice_mode,
    get_available_voices,
    stop_speaking,
    test_tts,
    speak_async
)
from .math_reader import solve_math_problem, read_formula, preprocess_math_expression
from .desktop_control import (
    open_app,
    open_website,
    enable_accessibility,
    get_available_applications
)
from .multi_modal import process_multimodal_input
from .content_search import search_content
from .study_planner import add_event, set_reminder
from .qa_tutoring import answer_question, quiz_mode
from .offline_mode import enable_offline_mode, disable_offline_mode
from .offline_conversation import chat_with_ai, get_conversation_stats, save_session

# Voice commands module (requires speech_recognition)
try:
    from .voice_commands import (
        listen_for_command,
        process_desktop_command,
        listen_for_continuous_conversation,
        get_conversation_context
    )
except ImportError:
    # Voice commands not available due to missing speech_recognition
    pass

# Optional modules with external dependencies
try:
    from .braille import text_to_braille, braille_to_text
except ImportError:
    # Braille functions not available
    pass
