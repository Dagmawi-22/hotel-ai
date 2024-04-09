import spacy
from nltk.corpus import wordnet
import json
import os

class IntentClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.intents = self._load_intents()

    def _load_intents(self):
        file_path = os.path.join(os.path.dirname(__file__), 'intents.json')
        with open(file_path) as file:
            intents = json.load(file)
        return intents

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
        for token in doc:
            for intent, keywords in self.intents.items():
                for keyword in keywords:
                    keyword_forms = [keyword, keyword + 's']  
                    for form in keyword_forms:
                        if token.text.lower() == form.lower() or token.text.lower() in self._get_synonyms(form):
                            return intent
        return "unknown"
