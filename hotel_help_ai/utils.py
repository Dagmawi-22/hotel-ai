from spellchecker import SpellChecker

def correct_spelling(sentence):
    spell = SpellChecker()
    words = sentence.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_sentence = ' '.join(corrected_words)
    return corrected_sentence