"""
Account API Service Test Suite

Run with:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import logging
import os
from unittest import TestCase

from service import create_app, talisman
from service.common import status
from service.models import Account, db
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"
HTTPS_ENVIRON = {"wsgi.url_scheme": "https"}


class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.app.config["DEBUG"] = False
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        cls.app.logger.setLevel(logging.CRITICAL)

        # Disable HTTPS enforcement for tests
        talisman.force_https = False

        # Flask test client
        cls.client = cls.app.test_client()

        # Ensure DB is clean and available
        with cls.app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        """Run before each test"""
        with self.app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def tearDown(self):
        """Run after each test"""
        with self.app.app_context():
            db.session.remove()

    def _create_accounts(self, count):
        """Factory method to create accounts"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    def test_index(self):
        """It should get 200_OK from the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "OK")

    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL, json=account.serialize(), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_security_headers(self):
        """It should return security headers"""
        response = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_internal_server_error(self):
        """It should return a 500 Internal Server Error"""
        self.app.config["PROPAGATE_EXCEPTIONS"] = False
        response = self.client.get(
            "/boom", environ_overrides={"wsgi.url_scheme": "https"}
        )
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data["error"], "Internal Server Error")
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def test_cors_security(self):
        """It should return a CORS header"""
        response = self.client.get("/", environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check for the CORS header
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"), "*"
        )
