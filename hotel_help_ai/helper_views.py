from django.http import JsonResponse

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