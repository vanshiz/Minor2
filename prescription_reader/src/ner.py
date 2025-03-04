# ner_processing.py
import spacy
from spacy.matcher import Matcher

def load_custom_nlp_model():
    """Load spaCy's en_core_web_sm model (you can change this if SciSpaCy becomes available)."""
    try:
        nlp = spacy.load("en_core_web_sm")
        print("Loaded spaCy's en_core_web_sm model.")
    except OSError:
        nlp = spacy.load("en_core_web_sm")
        print("Using fallback spaCy model.")
    return nlp

def create_matcher(nlp):
    """Create a Matcher with custom patterns for drugs, dosages, and frequency."""
    matcher = Matcher(nlp.vocab)
   
    drug_patterns = [
        [{"LOWER": "paracetamol"}],
        [{"LOWER": "ibuprofen"}],
        [{"LOWER": "aspirin"}],
        [{"LOWER": "digoxin"}]
    ]
    for pattern in drug_patterns:
        matcher.add("DRUG", [pattern])
   
    matcher.add("DOSAGE", [[{"TEXT": {"REGEX": r"\d+mg"}}]])
    
    matcher.add("FREQUENCY", [[{"LOWER": "twice"}, {"LOWER": "daily"}]])
    
    return matcher

def extract_entities(text, nlp=None, matcher=None):
    """Extracts drugs, dosages, and frequency from text using a custom Matcher."""
    if nlp is None:
        nlp = load_custom_nlp_model()
    if matcher is None:
        matcher = create_matcher(nlp)
    
    doc = nlp(text)
    matches = matcher(doc)
   
    extracted_info = {"DRUG": [], "DOSAGE": [], "FREQUENCY": []}
    
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        extracted_info[label].append(doc[start:end].text)
    return extracted_info

