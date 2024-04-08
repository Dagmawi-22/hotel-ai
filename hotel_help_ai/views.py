from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import spacy

@csrf_exempt
def chatbot_api(request):
    if request.method == "GET":
        return JsonResponse({"message": "Welcome to the Hotel Chatbot API!"})
    elif request.method == "POST":
        data = request.POST
        question = data.get("question", "")
        
        chatbot = HotelChatbot()
        answer = chatbot.predict_answer(question)
        
        return JsonResponse({"question": question, "answer": answer})

class HotelChatbot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")  # Load spaCy NLP model

    def predict_answer(self, question):
        # Implement NLP processing
        doc = self.nlp(question)

        # Implement intent classification
        intent = self.classify_intent(doc)

        # Generate response based on intent
        response = self.generate_response(intent)

        return response

    def classify_intent(self, doc):
        # Implement intent classification logic
        # You can use spaCy's text classification capabilities or train a separate classifier
        # For example:
        # intent = some_classification_function(doc)
        intent = "book_room"  # Dummy intent for illustration

        return intent

    def generate_response(self, intent):
        # Implement logic to generate response based on intent
        # Use templates or generate responses dynamically based on the detected intent and entities
        # For example:
        if intent == "book_room":
            response = "Sure, I can help you with booking a room. Could you please provide me with your check-in and check-out dates?"
        else:
            response = "I'm sorry, I didn't understand that. Can you please rephrase your question?"

        return response
