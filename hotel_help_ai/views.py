from django.http import JsonResponse
from .classifier import IntentClassifier
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import random





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
    responses = {
        'book_room': [
            "Sure, I can help you with booking a room. Could you please provide me with your check-in and check-out dates?",
            "Let's get started with booking your room. When are you planning to check-in and check-out?",
            "Booking a room is no problem! Please let me know your preferred dates.",
            "I'm here to assist you with booking. Let's begin with your check-in and check-out dates.",
            "Booking a room? Count on me! Just tell me when you want to check-in and check-out.",
            "No worries, I'll help you book a room. Please provide your check-in and check-out dates.",
            "Booking made easy! Tell me your check-in and check-out dates to get started.",
            "I'm ready to assist you with room booking. When do you plan to check-in and check-out?",
            "Need a room booked? I'm here to help. Give me your check-in and check-out dates.",
            "Let's book a room! Just share your check-in and check-out dates with me."
        ],
        'check_availability': [
            "Checking room availability...",
            "Let me check the availability of rooms for you.",
            "Checking available rooms...",
            "I'll verify the room availability right away.",
            "Confirming room availability...",
            "Just a moment, I'll check the room availability.",
            "Checking for available rooms...",
            "Let's see if we have any rooms available.",
            "Verifying room availability...",
            "Checking our room inventory..."
        ],
        'room_service_request': [
            "What would you like to order for room service?",
            "I'm here to assist you with room service. What can I get for you?",
            "Ready to take your room service order! What would you like?",
            "Making room service easy! Let me know your order.",
            "Room service is just a message away! What can I assist you with?",
            "Feel free to order room service! What's your preference?",
            "Tell me what you'd like for room service, and I'll take care of the rest.",
            "Room service request noted! What's your order?",
            "Let's make your room service request! What can I arrange for you?",
            "Your room service request is my command! What do you need?"
        ],
        'amenities_inquiry': [
            "Here are the amenities available at our hotel...",
            "Let me provide you with information about the amenities we offer.",
            "Discover our hotel amenities...",
            "I'll share details about our hotel amenities with you.",
            "Exploring hotel amenities? I can help!",
            "Learn more about our hotel amenities...",
            "Here's what our hotel has to offer in terms of amenities.",
            "I'll outline the amenities available at our hotel for you.",
            "Curious about our hotel amenities? I've got you covered!",
            "Let's explore the amenities provided by our hotel."
        ],
        'local_attractions': [
            "You might enjoy visiting these local attractions...",
            "Here are some nearby attractions you might find interesting.",
            "Discover local attractions near our hotel...",
            "I'll suggest some local attractions worth exploring.",
            "Exploring the area? Check out these local attractions!",
            "Let me recommend some nearby attractions for you to visit.",
            "Here's a list of local attractions you can explore.",
            "Discover what the local area has to offer in terms of attractions.",
            "Looking for things to do nearby? Check out these local attractions!",
            "Explore nearby attractions to make the most of your stay."
        ],
        'restaurant_reservations': [
            "Would you like to make a reservation at our restaurant?",
            "Let's make a reservation for you at our restaurant. When would you like to dine?",
            "Reserve a table at our restaurant for a delightful dining experience!",
            "I can help you make a reservation at our restaurant. What time suits you?",
            "Planning to dine at our restaurant? Let's secure your reservation!",
            "Reserve your table now for an unforgettable dining experience at our restaurant!",
            "Book a table at our restaurant for your upcoming meal!",
            "I'll assist you in making a reservation at our restaurant. When are you available?",
            "Secure your spot at our restaurant by making a reservation now!",
            "Looking to dine with us? Let's reserve a table for you!"
        ],
        'hi': [
            "Hi there.",
            "Hello!",
            "Hey!",
            "Hi, how can I assist you today?",
            "Hello there! How can I help?",
            "Greetings!",
            "Hi! What brings you here?",
            "Hey there! Ready to chat?",
            "Hello! I'm here to help. What do you need?",
            "Hi! Let me know how I can assist you."
        ],
        'default': [
            "I'm sorry, I didn't understand that.",
            "Apologies, I couldn't comprehend your query.",
            "I'm not sure I understand. Could you please rephrase?",
            "Could you provide more details? I want to assist you effectively.",
            "I'm here to help, but I'm not sure what you're asking. Can you clarify?",
            "I'm having trouble understanding. Can you provide more information?",
            "I'm afraid I didn't catch that. Can you please repeat or rephrase?",
            "Sorry, I didn't get that. Can you provide more context?",
            "I'm a bit confused. Can you give me more details?",
            "I'm not sure what you mean. Can you elaborate?"
        ]
    }

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
