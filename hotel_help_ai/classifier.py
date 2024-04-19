import os
import json
import spacy
from nltk.corpus import wordnet
from collections import defaultdict

class IntentClassifier:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.intents = self._load_intents()
        self.intent_memory = self._load_intent_memory()

    def _load_intents(self):
        file_path = os.path.join(os.path.dirname(__file__), 'intents.json')
        with open(file_path) as file:
            intents = json.load(file)
        return intents

    def _load_intent_memory(self):
        file_path = os.path.join(os.path.dirname(__file__), 'intent_memory.json')
        if os.path.exists(file_path):
            with open(file_path) as file:
                intent_memory = json.load(file)
        else:
            intent_memory = {}
        return intent_memory

    def _update_intent_memory(self):
        file_path = os.path.join(os.path.dirname(__file__), 'intent_memory.json')
        with open(file_path, 'w') as file:
            json.dump(self.intent_memory, file, indent=2)

    def classify_intent(self, query, requester_ip):
        doc = self.nlp(query)
        detected_intent, confidence, greet = self._classify_intent_from_query(doc, requester_ip)

        if detected_intent.lower() == 'bye':
            self.clear_current_intent(requester_ip)
        else:
            self._set_current_intent(requester_ip, detected_intent)
            self._update_intent_memory()

        stored_intent = self._get_current_intent(requester_ip)
        if detected_intent != 'unknown':
            return {"intent": detected_intent, "confidence": confidence, "greet": greet}
        elif stored_intent:
            return {"intent": stored_intent, "confidence": 100, "greet": greet}
        else:
            return {"intent": "unknown", "confidence": None, "greet": greet}

    def _get_synonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonym = lemma.name().lower()
                synonyms.add(synonym)
                if '_' in synonym:  
                    compound_word = synonym.replace('_', ' ')
                    if compound_word.endswith('s'):
                        synonyms.add(compound_word.lower())
                else:  
                    synonyms.add(synonym + 's')
        return synonyms

    def _classify_intent_from_query(self, doc, requester_ip):
        intent_scores = defaultdict(int)
        total_words = 0
        detected_intent = "unknown"
        confidence = None
        greet = False

    # First pass to classify intents
        for token in doc:
            total_words += 1
            for intent, words_dict in self.intents.items():
                primary_words = words_dict.get("primary", [])
                secondary_words = words_dict.get("secondary", [])
                all_words = primary_words + secondary_words
                if token.text.lower() in (primary_words + [syn for word in primary_words for syn in self._get_synonyms(word)]):
                    if intent_scores[intent] == 0:
                        intent_scores[intent] = len(primary_words) + len(secondary_words)
                    else:
                        intent_scores[intent] += 1

        if intent_scores:
            if "greeting" in intent_scores:
                print("Greeting intent found with a score of:", intent_scores)
                greet = True
            max_score = max(intent_scores.values())
            max_intents = [intent for intent, score in intent_scores.items() if score == max_score]
            if len(max_intents) == 1:
                print("got this", max_intents)
                detected_intent = max_intents[0]
            elif "greetings" in max_intents:
                greet = True
                print("greeeet", greet)
                max_intents.remove("greetings")
                detected_intent = max_intents[0]

            if detected_intent != "unknown":
                confidence = (intent_scores[detected_intent] / total_words) * 100
                confidence = min(confidence, 100)

            if detected_intent == "greetings":
                greet = True
                intent_scores.pop("greetings", None)
                if intent_scores:
                    max_score = max(intent_scores.values())
                    max_intents = [intent for intent, score in intent_scores.items() if score == max_score]
                    if len(max_intents) > 0:
                        detected_intent = max_intents[0]

                        # Calculate confidence
                        if detected_intent != "unknown":
                            confidence = (intent_scores[detected_intent] / total_words) * 100
                            confidence = min(confidence, 100)

            current_intent = self._get_current_intent(requester_ip)
            if current_intent and detected_intent != current_intent:
                self._set_current_intent(requester_ip, detected_intent)
                self._update_intent_memory()

        return detected_intent, confidence, greet


    def _get_current_intent(self, requester_ip):
        return self.intent_memory.get(requester_ip, None)

    def _set_current_intent(self, requester_ip, intent):
        self.intent_memory[requester_ip] = intent

    def clear_current_intent(self, requester_ip):
        if requester_ip in self.intent_memory:
            del self.intent_memory[requester_ip]
            self._update_intent_memory()
