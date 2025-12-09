import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gemini_dm import GeminiDM

class TestSupervise(unittest.TestCase):
    @patch('src.gemini_dm.get_api_key')
    @patch('src.gemini_dm.genai')
    def test_supervise_does_not_send_message_when_not_started(self, mock_genai, mock_get_api_key):
        # Setup mocks
        mock_get_api_key.return_value = "fake_key"
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        dm = GeminiDM()

        # Ensure started is False initially
        self.assertFalse(dm.started)

        # Call supervise
        response = dm.supervise()

        # VERIFICATION: The bug fix should prevent sending a message if not started.
        mock_chat.send_message.assert_not_called()
        self.assertEqual(response, "Game has not started yet.")

        # And started is still False
        self.assertFalse(dm.started)

if __name__ == '__main__':
    unittest.main()
