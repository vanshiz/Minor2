# spell_correction.py
import pkg_resources
from symspellpy.symspellpy import SymSpell, Verbosity

def init_sym_spell(max_edit_distance=2, prefix_length=7):
    """Initialize SymSpell and load the default dictionary."""
    sym_spell = SymSpell(max_edit_distance, prefix_length)
    dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
    return sym_spell

def load_medicine_terms(sym_spell, medicine_terms_file):
    """Load medicine terms from a file and add them to the SymSpell dictionary."""
    try:
        with open(medicine_terms_file, "r", encoding="utf-8") as f:
            medicine_terms = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(medicine_terms)} medicine terms from {medicine_terms_file}.")
    except Exception as e:
        print(f"Failed to load medicine terms from {medicine_terms_file}: {e}")
        medicine_terms = []
    
    for term in medicine_terms:
        sym_spell.create_dictionary_entry(term, 1)
    return sym_spell

def correct_text(text, sym_spell, max_edit_distance=2):
    """Correct the text word-by-word using SymSpell."""
    words = text.split()
    corrected_words = []
    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance)
        if suggestions:
            corrected_words.append(suggestions[0].term)
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)
