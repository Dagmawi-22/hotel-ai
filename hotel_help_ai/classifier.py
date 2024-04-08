import spacy
from nltk.corpus import wordnet

class IntentClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def classify_intent(self, query):
        doc = self.nlp(query)
        intent = self._classify_intent_from_query(doc)
        return intent

    def _get_synonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
                
                if '_' in lemma.name():  
                    compound_word = lemma.name().replace('_', ' ')
                    if compound_word.endswith('s'):
                        synonyms.add(compound_word.lower())
                else:  
                    synonyms.add(lemma.name().lower() + 's')
        return synonyms

    def _classify_intent_from_query(self, doc):
        intents = {
            "book_room": ["book", "reserve", "room"],
            "hi": ["hey", "hi", "hi there"],
            "check_availability": ["available", "availability"],
            "room_service_request": ["service", "request", "room"],
            "amenities_inquiry": ["amenity"],
            "local_attractions": ["attraction", "site"],
            "restaurant_reservations": ["reservation", "restaurant", "reserve", "res"]
        }

        for token in doc:
            for intent, keywords in intents.items():
                for keyword in keywords:
                    keyword_forms = [keyword, keyword + 's']  
                    for form in keyword_forms:
                        if token.text.lower() == form.lower() or token.text.lower() in self._get_synonyms(form):
                            return intent

        return "unknown"
