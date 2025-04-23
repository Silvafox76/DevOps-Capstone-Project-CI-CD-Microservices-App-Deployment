"""
Error Handlers for the Account Service
"""

from flask import current_app, jsonify
from service.common import status
from service.models import DataValidationError


def init_error_handlers(app):
    """Register all error handlers with the Flask app."""

    @app.errorhandler(DataValidationError)
    def request_validation_error(error):
        """Handle DataValidationError with 400 response"""
        current_app.logger.warning(f"Validation error: {str(error)}")
        return bad_request(error)

    @app.errorhandler(status.HTTP_400_BAD_REQUEST)
    def bad_request(error):
        """Handle 400 Bad Request"""
        current_app.logger.warning(f"400 Bad Request: {str(error)}")
        return (
            jsonify(
                status=status.HTTP_400_BAD_REQUEST,
                error="Bad Request",
                message=str(error),
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    @app.errorhandler(status.HTTP_404_NOT_FOUND)
    def not_found(error):
        """Handle 404 Not Found"""
        current_app.logger.warning(f"404 Not Found: {str(error)}")
        return (
            jsonify(
                status=status.HTTP_404_NOT_FOUND,
                error="Not Found",
                message=str(error),
            ),
            status.HTTP_404_NOT_FOUND,
        )

    @app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
    def method_not_supported(error):
        """Handle 405 Method Not Allowed"""
        current_app.logger.warning(f"405 Method Not Allowed: {str(error)}")
        return (
            jsonify(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                error="Method Not Allowed",
                message=str(error),
            ),
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    def mediatype_not_supported(error):
        """Handle 415 Unsupported Media Type"""
        current_app.logger.warning(
            f"415 Unsupported Media Type: {str(error)}"
        )
        return (
            jsonify(
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                error="Unsupported Media Type",
                message=str(error),
            ),
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle generic 500 Internal Server Error"""
        current_app.logger.error(f"500 Internal Server Error: {str(error)}")
        return (
            jsonify(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error="Internal Server Error",
                message=(
                    "An unexpected error occurred. "
                    "Please try again later."
                ),
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
