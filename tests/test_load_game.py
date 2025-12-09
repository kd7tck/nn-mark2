import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gemini_dm import GeminiDM
from src.game import Game

class TestLoadGame(unittest.TestCase):
    @patch('src.gemini_dm.get_api_key')
    @patch('src.gemini_dm.genai')
    def test_load_save_state_returns_text_and_updates_history(self, mock_genai, mock_get_api_key):
        # Setup mocks
        mock_get_api_key.return_value = "fake_key"

        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        # Mock the response from send_message
        mock_response = MagicMock()
        expected_dm_text = "The game is restored. You are standing in the town square."
        mock_response.text = expected_dm_text
        mock_chat.send_message.return_value = mock_response

        # Initialize Game (which initializes GeminiDM)
        # We need to mock pygame because Game.__init__ calls pygame.init() and sets up display
        with patch('src.game.pygame'):
            game = Game()

            # Mock the file reading for load_game
            # We need to mock os.path.exists and open
            with patch('src.game.os.path.exists', return_value=True):
                with patch('src.game.open', unittest.mock.mock_open(read_data='{"display_history": ["Old history"], "dm_save_data": "save data"}')):
                     # Call load_game
                    result = game.load_game()

                    # Verify result
                    self.assertEqual(result, "Game loaded successfully.")

                    # Verify history was updated
                    # It should contain: "Old history" and "DM: The game is restored..."
                    self.assertIn("Old history", game.history)
                    self.assertIn(f"DM: {expected_dm_text}", game.history)

                    # Verify gemini.load_save_state returned the text
                    # We can't easily check the return value of the internal call, but we checked the effect (history update)

    @patch('src.gemini_dm.get_api_key')
    @patch('src.gemini_dm.genai')
    def test_load_save_state_method_returns_text(self, mock_genai, mock_get_api_key):
         # Setup mocks
        mock_get_api_key.return_value = "fake_key"

        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_model.start_chat.return_value = mock_chat

        # Mock the response from send_message
        mock_response = MagicMock()
        expected_text = "Restored."
        mock_response.text = expected_text
        mock_chat.send_message.return_value = mock_response

        gemini = GeminiDM()
        result = gemini.load_save_state("data")
        self.assertEqual(result, expected_text)

if __name__ == '__main__':
    unittest.main()
