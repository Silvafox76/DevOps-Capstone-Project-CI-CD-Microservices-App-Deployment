"""
Tests for CLI Commands
"""
from unittest import TestCase
from service import create_app

class TestCLICommands(TestCase):
    """Tests for CLI Commands"""

    def setUp(self):
        """Create app instance for CLI runner"""
        self.app = create_app()
        self.runner = self.app.test_cli_runner()

    def test_db_create(self):
        """It should call the db-create command successfully"""
        result = self.runner.invoke(args=["db-create"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Database created", result.output)
