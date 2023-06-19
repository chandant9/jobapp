from django.shortcuts import redirect


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path_info.startswith('/login/'):
            return redirect('login')
        return self.get_response(request)