from .classifier import IntentClassifier
from django.views.decorators.csrf import csrf_exempt
import random
import os
import json
from .helper_views import response_handler
from .utils import correct_spelling

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        # Decode the request body and load it as JSON
        data = json.loads(request.body.decode('utf-8'))
        print("Data received:", data)
        user_query = data.get('query', '')

        if not user_query: 
            return response_handler('Query cannot be empty', False, 400)
        
        user_query = correct_spelling(user_query)
        
        intent_classifier = IntentClassifier()
        intent_response = intent_classifier.classify_intent(user_query)
        
        print("User query:", user_query)
        print("Detected Intent:", intent_response['intent'])

        response_data = {
            'question':  user_query,
            'intent': intent_response['intent'],
        }
        
        if 'confidence' in intent_response:
            response_data['confidence'] = intent_response['confidence']
        
        response = generate_response(intent_response['intent'])

        response_data['response'] = response

        return response_handler(response_data, True, 200)
    else:
        return response_handler('Invalid request method. Supported method for this route: POST', False, 422)

def generate_response(intent):
    responses_file_path = os.path.join(os.path.dirname(__file__), 'responses.json')
    with open(responses_file_path) as file:
        responses = json.load(file)

    if intent in responses:
        response = random.choice(responses[intent])
    else:
        response = random.choice(responses['default'])

    return response
