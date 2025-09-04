from django.shortcuts import redirect
from django.urls import reverse


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


class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Пропускаем анонимных пользователей и определенные URL
        if not request.user.is_authenticated:
            return None

        # URL, которые не требуют подтверждения email
        exempt_urls = [
            reverse('logout'),
            reverse('verification'),
            reverse('verification_sent'),
            # Не включаем verify_email сюда, так как он требует аргумент code
        ]

        if request.path.startswith('/user/verify/'):  # Разрешаем все verify URLs
            return None

        if request.path in exempt_urls:
            return None

        # Проверяем, подтвержден ли email
        if (request.user.is_authenticated and
            not request.user.email_verified and
            not request.user.is_staff):
            return redirect('verification')

        return None
