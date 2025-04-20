import re
import spacy
import sys

# Regex patterns for specific PII types
REGEX_PATTERNS = {
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b",
    "phone_number": r"\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b",  # More specific pattern
    "dob": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "aadhar_num": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\bCVV\s*:?\s*\d{3}\b",  # Make CVV pattern more specific
    "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2}|[0-9]{4})\b"
}

# spaCy label map to our required entity type
SPACY_ENTITY_MAP = {
    "PERSON": "full_name"
}

# Try to load spaCy model, with fallback if not available
try:
    nlp = spacy.load("en_core_web_sm")
    use_spacy = True
except IOError:
    print("Warning: spaCy model 'en_core_web_sm' not found.")
    print("Install it using: python -m spacy download en_core_web_sm")
    print("Continuing with regex-only PII detection...")
    use_spacy = False


def mask_pii(text: str):
    """
    Masks PII in a given email using regex and spaCy NER.
    """
    masked_entities = []
    replacements = []

    # Step 1: Regex-based masking
    for entity_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            entity_text = match.group()
            start, end = match.start(), match.end()
            replacements.append((start, end, entity_type, entity_text))

    # Step 2: spaCy-based NER (e.g., for names) - only if model is available
    if use_spacy:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in SPACY_ENTITY_MAP:
                entity_type = SPACY_ENTITY_MAP[ent.label_]
                start, end = ent.start_char, ent.end_char
                entity_text = ent.text
                replacements.append((start, end, entity_type, entity_text))

    # Step 3: Sort by length (longer matches first), then by start index
    replacements = sorted(replacements, key=lambda x: (-(x[1] - x[0]), x[0]))

    # Step 4: Handle overlapping entities
    masked_text = text
    masked_positions = set()  # Keep track of already masked positions

    final_replacements = []
    for start, end, entity_type, entity_text in replacements:
        # Check if this segment overlaps with any already masked segment
        overlap = False
        for pos in range(start, end):
            if pos in masked_positions:
                overlap = True
                break

        if not overlap:
            # Add this replacement to the final list
            final_replacements.append((start, end, entity_type, entity_text))
            # Mark all positions as masked
            for pos in range(start, end):
                masked_positions.add(pos)

    # Step 5: Sort by start index (reverse for safe replacement)
    final_replacements = sorted(final_replacements, key=lambda x: x[0], reverse=True)

    masked_text = text
    for start, end, entity_type, entity_text in final_replacements:
        masked_text = masked_text[:start] + f"[{entity_type}]" + masked_text[end:]
        masked_entities.append({
            "position": [start, end],
            "classification": entity_type,
            "entity": entity_text
        })

    # Reverse the entity list (to preserve order as per appearance)
    masked_entities.reverse()

    return {
        "input_email_body": text,
        "list_of_masked_entities": masked_entities,
        "masked_email": masked_text,
        "category_of_the_email": None  # will be filled later after classification
    }


# For testing
if __name__ == "__main__":
    email = """
        Hello, my name is John Doe. I was born on 05/06/1992.
        You can reach me at john.doe@gmail.com or +91-9876543210.
        My Aadhar number is 1234 5678 9012 and card number is 1234-5678-9101-1121.
        CVV: 123 Expiry: 09/25
    """

    result = mask_pii(email)
    from pprint import pprint
    pprint(result)