def jwt_response_payload_handler(token, user=None, request=None, pk=None):
    return {
        'code': 20000,
        'data': {
            'token': token,
            'pk': pk,
            'from': 'django'
        }
    }
