# middleware.py
from django.middleware.csrf import CsrfViewMiddleware

class MobileCsrfExemptMiddleware(CsrfViewMiddleware):
    def process_request(self, request):
        # Check for a custom header identifying mobile requests
        if 'X-Mobile-App' in request.headers:  # You can use any header that the mobile app sends
            return None  # Skip CSRF check for mobile requests
        return super().process_request(request)
