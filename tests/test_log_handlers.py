import unittest
from unittest.mock import MagicMock
from service.common.log_handlers import init_logging

class TestLogHandlers(unittest.TestCase):
    def test_init_logging(self):
        """It should initialize logging with formatter"""
        mock_app = MagicMock()
        mock_logger = MagicMock()
        mock_handler = MagicMock()

        # Setup fake logger
        mock_logger.handlers = [mock_handler]
        mock_logger.level = 20  # INFO

        # Patch the logger inside the function
        with unittest.mock.patch("logging.getLogger", return_value=mock_logger):
            init_logging(mock_app, "test.logger")

        # Assertions
        mock_app.logger.setLevel.assert_called_with(20)
        mock_handler.setFormatter.assert_called()
