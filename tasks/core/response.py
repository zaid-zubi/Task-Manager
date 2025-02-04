from rest_framework.response import Response

def http_response(data, status_code, message):
    return Response({
        "data": data,
        "status": status_code,
        "message": message
    })

def http_error_response(errors, status_code, message):
    return Response({
        "error": errors,
        "status": status_code,
        "message": message
    })