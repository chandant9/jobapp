from django.shortcuts import redirect


class AuthenticationMiddleware:
    EXCLUDED_URLS = ('/home/',
                     '/login/',
                     '/register/',
                     '/register/role_selection/',
                     '/register/candidate_register/',
                     '/register/recruiter_register/',
                     '/job-details/',
                     '/job-details/<int:job_id>/',
                     '/api/jobs/',
                     '/api/job-details/',
                     '/api/role-selection/',
                     '/api/register/candidate/',
                     '/api/register/recruiter/',
                     '/api/login/',
                     '/api/logout/',
                     )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path_info.startswith(self.EXCLUDED_URLS):
            return redirect('home')
        return self.get_response(request)
