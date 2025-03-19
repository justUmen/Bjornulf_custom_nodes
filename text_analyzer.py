import re
import subprocess
import sys

# Load the spaCy model once globally to keep it lightweight
def ensure_model(model_name="en_core_web_sm"):
    try:
        # Try to load the model
        import spacy
        spacy.load(model_name)
    except OSError:
        # If the model isn't found, download it
        print(f"Model '{model_name}' not found. Downloading now...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        print(f"Model '{model_name}' downloaded successfully.")

class TextAnalyzer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True})
            }
        }

    # Define the output types and their names
    RETURN_TYPES = ("INT", "INT", "INT", "STRING", "STRING", "FLOAT", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("number_lines", "number_words", "number_characters", "language", "sentiment", "sentiment_polarity", "type", "character", "sentence", "subject", "action", "target")

    FUNCTION = "analyze"
    CATEGORY = "Bjornulf"

    def analyze(self, text):
        from langdetect import detect
        from textblob import TextBlob
        import spacy
        
        ensure_model()
        nlp = spacy.load("en_core_web_sm")
        # **Statistics**
        # Count lines by splitting on newline characters
        lines = len(text.split('\n'))
        # Count words by splitting on whitespace
        words = len(text.split())
        # Count total characters including spaces and punctuation
        characters = len(text)

        # **Dialog or Description Detection**
        # Check if the text starts with a name followed by a colon (e.g., "Jessica:")
        dialog_match = re.match(r'^([A-Za-z]+):', text)
        if dialog_match:
            type_ = 'dialog'
            character = dialog_match.group(1)  # Extract the character name
            spoken_text = text[dialog_match.end():].strip()  # Text after the colon
        else:
            type_ = 'description'
            character = None
            spoken_text = text

        # **Language Detection**
        try:
            language = detect(spoken_text)
        except:
            language = 'unknown'

        # **Sentiment Analysis**
        blob = TextBlob(spoken_text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = 'positive'
        elif polarity < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        # **Subject, Action, Target Extraction**
        # Only perform NLP if the language is English (for spaCy compatibility)
        if language == 'en':
            doc = nlp(spoken_text)
            action = None
            subject = None
            target = None
            # Look for the main verb (action) and its subject and object
            for token in doc:
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                    action = token.text
                    subject_tokens = [w for w in token.children if w.dep_ == 'nsubj']
                    target_tokens = [w for w in token.children if w.dep_ == 'dobj']
                    if subject_tokens:
                        subject = subject_tokens[0].text
                    if target_tokens:
                        target = target_tokens[0].text
                    break
        else:
            subject, action, target = None, None, None

        # **Return Results**
        # Convert None to empty strings for ComfyUI compatibility
        return (
            lines,
            words,
            characters,
            language,
            sentiment,
            polarity,
            type_,
            character or "",
            spoken_text or "",
            subject or "",
            action or "",
            target or ""
        )