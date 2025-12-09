import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gemini_dm import GeminiDM

class TestStartGameFailure(unittest.TestCase):
    @patch('src.gemini_dm.genai')
    @patch('src.gemini_dm.get_api_key')
    def test_start_game_failure_resets_started_flag(self, mock_get_api_key, mock_genai):
        # Setup mock
        mock_get_api_key.return_value = "fake_key"

        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        # Initialize DM
        dm = GeminiDM()

        # Verify initialization
        self.assertTrue(dm.is_ready())
        self.assertFalse(dm.started)

        # Simulate network failure during start_game
        mock_chat.send_message.side_effect = Exception("Network Error")

        response = dm.start_game()

        # Verify error response
        self.assertIn("Error communicating", response)

        # Expectation: started should be False because it failed.
        # This test will FAIL if the bug is present.
        self.assertFalse(dm.started, "dm.started should be False after failed start_game")

if __name__ == '__main__':
    unittest.main()
