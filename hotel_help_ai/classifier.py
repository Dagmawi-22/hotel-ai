import spacy

class IntentClassifier:
    def __init__(self):
        # Load the spaCy model for natural language processing
        self.nlp = spacy.load("en_core_web_sm")

    def classify_intent(self, query):
        # Process the user's query using spaCy
        doc = self.nlp(query)

        # Classify intent based on the query
        intent = self._classify_intent_from_query(doc)

        return intent

    def _classify_intent_from_query(self, doc):
        # Define intent classification rules based on linguistic patterns, entities, or keywords
        intents = {
            "book_room": ["book", "reserve", "room"],
            "hi": ["hey", "hi", "hi there"],
            "check_availability": ["available", "availability"],
            "room_service_request": ["service", "request", "room"],
            "amenities_inquiry": ["amenities"],
            "local_attractions": ["attractions"],
            "restaurant_reservations": ["reservations", "restaurant", "reserve", "res"]
        }

        # Check if any of the tokens in the query match the intent keywords
        for token in doc:
            for intent, keywords in intents.items():
                if any(keyword in token.text.lower() for keyword in keywords):
                    return intent

        # If no specific intent is detected, return a default intent
        return "unknown"
