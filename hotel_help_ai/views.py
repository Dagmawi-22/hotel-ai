from django.http import JsonResponse
from .classifier import IntentClassifier
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = request.POST
        user_query = data.get('query', '')

        # Initialize intent classifier
        intent_classifier = IntentClassifier()

        # Classify intent
        intent = intent_classifier.classify_intent(user_query)
        
        # Print the detected intent for debugging
        print("Detected Intent:", intent)

        # Generate response based on intent
        response = generate_response(intent)

        return JsonResponse({
            'response': response,
            'question': user_query
            })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_response(intent):
    # Generate response based on intent
    if intent == 'book_room':
        response = "Sure, I can help you with booking a room. Could you please provide me with your check-in and check-out dates?"
    elif intent == 'check_availability':
        response = "Checking room availability..."
    elif intent == 'room_service_request':
        response = "What would you like to order for room service?"
    elif intent == 'amenities_inquiry':
        response = "Here are the amenities available at our hotel..."
    elif intent == 'local_attractions':
        response = "You might enjoy visiting these local attractions..."
    elif intent == 'restaurant_reservations':
        response = "Would you like to make a reservation at our restaurant?"
    else:
        response = "I'm sorry, I didn't understand that."

    return response
