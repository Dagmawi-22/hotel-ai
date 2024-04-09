from django.http import JsonResponse
from .classifier import IntentClassifier
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import random
import os
import json



def correct_spelling(sentence):
    spell = SpellChecker()
    words = sentence.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_sentence = ' '.join(corrected_words)
    return corrected_sentence

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = request.POST
        user_query = data.get('query', '')

        if not user_query: 
            return response_handler('query can not be empty', False, 400)
        
        user_query = correct_spelling(user_query)

        intent_classifier = IntentClassifier()

        intent = intent_classifier.classify_intent(user_query)
        
        print("User query:", user_query)
        print("Detected Intent:", intent)

        response = generate_response(intent)

        data = {
            'question':  user_query,
            'response': response,
        }

        return response_handler(data, True, 200)
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

def response_handler(data, success, statusCode):
    if isinstance(data, dict):
        serialized_data = data
    else:
        serialized_data = {'message': data}

    return JsonResponse({
        'data':  serialized_data,
        'success': success,
        'statusCode': statusCode
    })
