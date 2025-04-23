"""
Package: service

This package initializes the Flask app, sets up configuration,
logging, database models, routes, and error handlers.
"""

import sys
from flask import Flask
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info("*" * 70)
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info("*" * 70)

# Import modules after app creation to avoid circular imports
# pylint: disable=wrong-import-position, cyclic-import
from service import models, routes  # noqa: F401
from service.common import error_handlers, cli_commands  # noqa: F401

# Initialize the database
try:
    models.init_db(app)
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)  # Required by Gunicorn to stop respawning workers

app.logger.info("Service initialized!")
