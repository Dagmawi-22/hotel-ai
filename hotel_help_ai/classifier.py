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
        # Implement your intent classification logic here
        # You can use spaCy's capabilities to extract entities or patterns for intent classification
        # For simplicity, let's assume a basic rule-based approach for illustration
        for token in doc:
            if token.text.lower() == "book" and doc[token.i + 1].text.lower() == "room":
                return "book_room"
            elif token.text.lower() == "availability" or token.text.lower() == "available":
                return "check_availability"
            elif token.text.lower() == "service" and doc[token.i + 1].text.lower() == "request":
                return "room_service_request"
            elif token.text.lower() == "amenities":
                return "amenities_inquiry"
            elif token.text.lower() == "attractions":
                return "local_attractions"
            elif token.text.lower() == "reservations":
                return "restaurant_reservations"

        # If no specific intent is detected, return a default intent
        return "unknown"
