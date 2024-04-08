import spacy

class IntentClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def classify_intent(self, query):
        doc = self.nlp(query)

        intent = self._classify_intent_from_query(doc)

        return intent

    def _classify_intent_from_query(self, doc):
        intents = {
            "book_room": ["book", "reserve", "room"],
            "hi": ["hey", "hi", "hi there"],
            "check_availability": ["available", "availability"],
            "room_service_request": ["service", "request", "room"],
            "amenities_inquiry": ["amenities"],
            "local_attractions": ["attractions"],
            "restaurant_reservations": ["reservations", "restaurant", "reserve", "res"]
        }

        for token in doc:
            for intent, keywords in intents.items():
                if any(keyword in token.text.lower() for keyword in keywords):
                    return intent

        return "unknown"
