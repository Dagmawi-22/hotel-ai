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

def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("ippp", ip)
    return ip
