from django.http import JsonResponse
from classifier import IntentClassifier

def chatbot(request):
    if request.method == 'POST':
        data = request.POST
        user_query = data.get('query', '')

        # Initialize intent classifier
        intent_classifier = IntentClassifier()

        # Classify intent
        intent = intent_classifier.classify_intent(user_query)

        # Logic to handle different intents
        if intent == 'book_room':
            # Logic to handle booking a room
            response = "I understand you want to book a room."
        elif intent == 'check_availability':
            # Logic to check room availability
            response = "Checking room availability..."
        elif intent == 'room_service_request':
            # Logic to handle room service requests
            response = "What would you like to order for room service?"
        elif intent == 'amenities_inquiry':
            # Logic to provide information about hotel amenities
            response = "Here are the amenities available at our hotel..."
        elif intent == 'local_attractions':
            # Logic to recommend local attractions or activities
            response = "You might enjoy visiting these local attractions..."
        elif intent == 'restaurant_reservations':
            # Logic to handle restaurant reservations
            response = "Would you like to make a reservation at our restaurant?"
        else:
            response = "Sorry, I didn't understand that."

        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
