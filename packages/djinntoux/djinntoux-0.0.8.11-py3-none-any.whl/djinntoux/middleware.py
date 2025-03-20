from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                timezone.activate(request.user.timezone)
            except AttributeError:
                timezone.deactivate()
        else:
             timezone.deactivate()