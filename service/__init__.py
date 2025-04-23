"""
Package: service

This module creates and configures the Flask app using the factory pattern.
"""

import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS  # ✅ Import CORS
from service import config
from service.models import init_db
from service.common import log_handlers
from service.common.error_handlers import init_error_handlers

# Global Talisman instance so it can be imported in tests
talisman = Talisman()

def create_app():
    """Application factory for initializing Flask app"""
    app = Flask(__name__)
    app.config.from_object(config)

    # Setup logging
    log_handlers.init_logging(app, "gunicorn.error")

    # Apply security headers
    talisman.init_app(app)

    # Enable CORS
    CORS(app)  # ✅ Now this is safe because `app` is defined

    # Register error handlers
    init_error_handlers(app)

    # Initialize the database
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

    # Logging banner
    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")
    app.logger.info("Service initialized!")

    return app

# Make importable for testing
__all__ = ["create_app", "talisman"]
