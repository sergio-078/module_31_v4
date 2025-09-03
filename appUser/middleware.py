class UserIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Сохраняем IP адрес в запросе для использования в сигналах
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.user_ip = x_forwarded_for.split(',')[0]
        else:
            request.user_ip = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)
        return response
