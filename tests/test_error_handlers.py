

from unittest import TestCase
from service import create_app
from service.common.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_415_UNSUPPORTED_MEDIA_TYPE
from service.models import DataValidationError

class TestErrorHandlers(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_bad_request_handler(self):
        with self.app.test_request_context():
            response = self.app.handle_user_exception(DataValidationError("Invalid data"))
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_not_found_handler(self):
        """It should return 404 Not Found"""
        response = self.client.get("/nonexistent", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_method_not_allowed_handler(self):
        """It should return 405 Method Not Allowed"""
        response = self.client.put("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_unsupported_media_type_handler(self):
        """It should return 415 Unsupported Media Type"""
        response = self.client.post(
            "/accounts",
            data="not-json",  
            content_type="text/plain",  
            environ_overrides={"wsgi.url_scheme": "https"}
        )
        self.assertEqual(response.status_code, HTTP_415_UNSUPPORTED_MEDIA_TYPE)


