import google.generativeai as genai
from src.config import get_api_key

class GeminiDM:
    def __init__(self):
        self.api_key = get_api_key()
        self.chat = None
        self.model = None

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.chat = self.model.start_chat(history=[])
            except Exception as e:
                print(f"Error initializing Gemini: {e}")

        self.system_prompt = (
            "You are a Dungeon Master for an Advanced Dungeons & Dragons 2nd Edition game. "
            "You will facilitate an interactive fiction experience. "
            "Start by helping the player initialize the world and their character. "
            "Follow the rules of AD&D 2nd Edition loosely but strictly adhere to the roleplay aspect. "
            "Keep responses concise enough to fit on a game screen (under 200 words if possible) unless a major description is needed. "
            "Do not use markdown formatting like bold or asterisks in your final output, just plain text suitable for a retro terminal display."
        )
        self.started = False

    def is_ready(self):
        return self.chat is not None

    def start_game(self):
        if not self.is_ready():
            return "Gemini API Key missing or invalid. Please check your .env file."

        self.started = True
        try:
            # We send the system prompt as the first message to prime the context
            response = self.chat.send_message(self.system_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"

    def supervise(self):
        if not self.is_ready():
            return "Gemini API Key missing or invalid."

        supervision_prompt = (
            "SYSTEM INSTRUCTION: You are deviating from the role of the AD&D 2nd Edition Dungeon Master "
            "or hallucinating details inconsistent with the game state. Stop immediately. "
            "Review the previous context. Return to the game. "
            "Summarize the current situation for the player and wait for their action. "
            "Maintain the persona strictly."
        )

        try:
            response = self.chat.send_message(supervision_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"

    def send_action(self, action):
        if not self.is_ready():
            return "Gemini API Key missing or invalid."

        if not self.started:
            return self.start_game()

        try:
            response = self.chat.send_message(action)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"
