from django.utils.deprecation import MiddlewareMixin
from htmlmin import minify


class CustomHTMLMinifyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the response content type is HTML
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            # Minify the HTML content
            response.content = minify(response.content.decode())
        return response
