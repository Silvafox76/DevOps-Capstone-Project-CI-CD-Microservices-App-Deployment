"""WSGI entry point for Gunicorn"""
from service import create_app

app = create_app()
