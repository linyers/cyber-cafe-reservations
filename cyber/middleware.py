import pytz


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "django_timezone" in request.COOKIES:
            timezone = pytz.timezone(request.COOKIES["django_timezone"])
            request.timezone = timezone
        else:
            request.timezone = pytz.utc

        response = self.get_response(request)
        return response
