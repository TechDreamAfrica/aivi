"""
Braille Display and Translation Support module
"""
# Basic Grade 1 Braille mapping for English letters, numbers, and space
_braille_alphabet = {
    'a': '\u2801', 'b': '\u2803', 'c': '\u2809', 'd': '\u2819', 'e': '\u2811',
    'f': '\u280b', 'g': '\u281b', 'h': '\u2813', 'i': '\u280a', 'j': '\u281a',
    'k': '\u2805', 'l': '\u2807', 'm': '\u280d', 'n': '\u281d', 'o': '\u2815',
    'p': '\u280f', 'q': '\u281f', 'r': '\u2817', 's': '\u280e', 't': '\u281e',
    'u': '\u2825', 'v': '\u2827', 'w': '\u283a', 'x': '\u282d', 'y': '\u283d', 'z': '\u2835',
    ' ': ' ',
    '1': '\u2801', '2': '\u2803', '3': '\u2809', '4': '\u2819', '5': '\u2811',
    '6': '\u280b', '7': '\u281b', '8': '\u2813', '9': '\u280a', '0': '\u281a',
    '.': '\u2832', ',': '\u2802', '?': '\u2826', '!': '\u2816', '-': '\u2824',
    ';': '\u2806', ':': '\u2812', "'": '\u2804', '"': '\u2814', '/': '\u282c',
}
_braille_to_text = {v: k for k, v in _braille_alphabet.items()}

def text_to_braille(text):
    """
    Convert plain text to Grade 1 Braille Unicode string.
    Only basic English letters, numbers, and some punctuation are supported.
    """
    result = []
    for char in text.lower():
        result.append(_braille_alphabet.get(char, '?'))
    braille_str = ''.join(result)
    print(f"[Braille] Translating to Braille: {text} => {braille_str}")
    return braille_str

def braille_to_text(braille):
    """
    Convert Grade 1 Braille Unicode string to plain text.
    Only basic English letters, numbers, and some punctuation are supported.
    """
    result = []
    for ch in braille:
        result.append(_braille_to_text.get(ch, '?'))
    text_str = ''.join(result)
    print(f"[Braille] Translating to text: {braille} => {text_str}")
    return text_str
