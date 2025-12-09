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

        
        try:
            # We send the system prompt as the first message to prime the context
            response = self.chat.send_message(self.system_prompt)
            self.started = True
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

    def get_history(self):
        """Returns the chat history in a serializable format."""
        if not self.chat:
            return []

        serialized_history = []
        for content in self.chat.history:
            parts = []
            for part in content.parts:
                # Assuming part has text attribute.
                # In google-generativeai, parts are usually objects with text property.
                if hasattr(part, 'text'):
                    parts.append({'text': part.text})

            serialized_history.append({
                'role': content.role,
                'parts': parts
            })
        return serialized_history

    def load_history(self, history_data):
        """Restores the chat session from history data."""
        if not self.model:
            return False

        try:
            # history_data should be a list of dicts compatible with start_chat
            self.chat = self.model.start_chat(history=history_data)
            self.started = True # Assuming if we load history, the game is started
            return True
        except Exception as e:
            print(f"Error loading history: {e}")
            return False

    def generate_save_state(self):
        if not self.is_ready():
            return None

        # Prompt for generating save data
        save_prompt = (
            "SYSTEM: PAUSE GAME. GENERATE SAVE STATE. "
            "Please summarize the entire current game state in plain English. "
            "You must include specific details for the following to ensure a complete save: "
            "1. Character: Name, Race, Class, Level, Experience Points. "
            "2. Ability Scores: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma. "
            "3. Status: Current and Max Hit Points, Status Effects (Buffs, Debuffs, Conditions). "
            "4. Equipment: Worn items (Armor, Weapons, Accessories), Carried items, Encumbrance level. "
            "5. Inventory: List of all items with counts and brief descriptions. "
            "6. Magic: Memorized Spells, Used Spells, Remaining spell slots, Active magical effects. "
            "7. Location: Region name, Specific area description, Environmental details. "
            "8. Time: Current date and time of day in the game world. "
            "9. Quests: Active quests, Completed quests, Current objectives. "
            "10. NPCs: Nearby NPCs, their attitudes/relationships to the player, active conversations. "
            "11. Narrative: A summary of recent events, immediate threats, and the current situation. "
            "This summary will be used to reload the game later, so be extremely comprehensive."
        )

        try:
            response = self.chat.send_message(save_prompt)
            return response.text
        except Exception as e:
            return f"Error generating save state: {e}"

    def load_save_state(self, save_data):
        if not self.model:
            return False

        try:
            # Start a new chat
            self.chat = self.model.start_chat(history=[])

            # Send system prompt first to re-establish persona
            self.chat.send_message(self.system_prompt)

            # Send the save data to restore context
            restore_prompt = (
                f"SYSTEM: RESTORE GAME. The game is being reloaded. "
                f"Here is the saved state summary: {save_data} "
                "Use this information to restore the game context. "
                "Acknowledge that the game is restored and describe the current scene to the player so they can continue."
            )
            self.chat.send_message(restore_prompt)

            self.started = True
            return True
        except Exception as e:
            print(f"Error loading save state: {e}")
            return False
