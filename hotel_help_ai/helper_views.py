import json, random, os
from django.http import JsonResponse, HttpRequest


def response_handler(data, success, statusCode):
    if isinstance(data, dict):
        serialized_data = data
    else:
        serialized_data = {'data': data}

    return JsonResponse({
        'data':  serialized_data,
        'success': success,
        'statusCode': statusCode
    })
    
def respond_with_greetings(data, success, statusCode):
    if isinstance(data, dict):
        serialized_data = data
    else:
        serialized_data = {'data': data}

    responses_file_path = os.path.join(os.path.dirname(__file__), 'responses.json')
    with open(responses_file_path) as file:
        responses = json.load(file)
        greetings = responses.get('greeting', [])

    random_greeting = random.choice(greetings)

    if 'response' in serialized_data:
        serialized_data['response']  = random_greeting + ' ' + serialized_data['response']
    else:
        serialized_data['response'] = random_greeting

    return JsonResponse({
        'data': serialized_data,
        'success': success,
        'statusCode': statusCode
    })

def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("ippp", ip)
    return ip
