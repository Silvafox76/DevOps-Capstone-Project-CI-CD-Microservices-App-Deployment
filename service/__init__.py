"""
Package: service

This package initializes the Flask app using the factory pattern.
"""

import sys
from flask import Flask
from flask_talisman import Talisman
from service import config
from service.common import log_handlers
from service.common.error_handlers import init_error_handlers
from service.models import init_db

# Global Talisman instance (used in tests to disable HTTPS)
talisman = Talisman()


def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config)

    # Setup logging
    log_handlers.init_logging(app, "gunicorn.error")

    # Register HTTPS headers
    talisman.init_app(app)

    # Register error handlers
    init_error_handlers(app)

    # Initialize database
    try:
        init_db(app)
    except Exception as error:  # pylint: disable=broad-except
        app.logger.critical("%s: Cannot continue", error)
        sys.exit(4)

    # Register routes
    from service.routes import api
    app.register_blueprint(api)

    # Register CLI commands
    from service.common.cli_commands import register_commands
    register_commands(app)

    # Log banner
    app.logger.info("*" * 70)
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info("*" * 70)
    app.logger.info("Service initialized!")

    return app


#  Export these for test imports
__all__ = ["create_app", "talisman"]
