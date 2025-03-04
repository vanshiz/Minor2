# main.py
import os
from spell_correction import init_sym_spell, load_medicine_terms, correct_text
from ner import extract_entities
from data_structuring import load_text, save_json

def main():
    input_file = os.path.join("outputs", "1.txt")
    output_json = os.path.join("outputs", "structured_data.json")
    medicine_terms_file = os.path.join("data", "medicalTerms.txt")
    

    extracted_text = load_text(input_file)
    
   
    sym_spell = init_sym_spell()
    sym_spell = load_medicine_terms(sym_spell, medicine_terms_file)
    

    corrected_text = correct_text(extracted_text, sym_spell)
  
    entities = extract_entities(corrected_text)
    
    
    result_data = {
        "corrected_text": corrected_text,
        "entities": entities
    }
  
    save_json(result_data, output_json)
    print(f"Structured data saved to {output_json}")

if __name__ == "__main__":
    main()
