import pygame
import sys
from src.gemini_dm import GeminiDM

# Constants
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 24
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (200, 200, 200)
INPUT_COLOR = (255, 255, 255)
INPUT_BG_COLOR = (50, 50, 50)
PADDING = 20

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gemini AD&D 2nd Ed.")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)

        self.gemini = GeminiDM()
        self.history = ["Welcome to AD&D 2nd Ed. Initializing Dungeon Master..."]

        self.input_text = ""
        self.running = True
        self.waiting_for_response = False

        # Try to start the game immediately
        self.start_game_async()

    def start_game_async(self):
        # In a real async environment we would thread this.
        # For this template, we will just call it.
        # Since this involves a network call, the UI will freeze.
        # A proper implementation would use threading.
        # We will add a simple text to indicate loading.
        self.history.append("Connecting to Gemini...")
        self.waiting_for_response = True
        # NOTE: In a real game loop, we shouldn't block.
        # But for simplicity in this template, we might block on the first frame or use a thread.
        # Let's use a very simple non-threaded approach for the template,
        # understanding it will block.
        try:
            response = self.gemini.start_game()
            self.history.append(f"DM: {response}")
        except Exception as e:
             self.history.append(f"Error: {e}")
        self.waiting_for_response = False


    def handle_input(self, event):
        if event.key == pygame.K_RETURN:
            if self.input_text.strip():
                user_action = self.input_text
                self.history.append(f"You: {user_action}")
                self.input_text = ""
                self.process_action(user_action)
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            self.input_text += event.unicode

    def process_action(self, action):
        self.waiting_for_response = True
        # Again, blocking call for simplicity.
        # In production, use threading.Thread(target=self.threaded_request, args=(action,)).start()
        try:
            response = self.gemini.send_action(action)
            self.history.append(f"DM: {response}")
        except Exception as e:
            self.history.append(f"Error: {e}")
        self.waiting_for_response = False

    def draw_text(self):
        y_offset = PADDING
        # Simple word wrap or line breaking
        # For now, just display the last few lines that fit

        lines_to_draw = []
        for entry in self.history:
            # Basic wrapping
            words = entry.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] < WIDTH - 2 * PADDING:
                    current_line = test_line
                else:
                    lines_to_draw.append(current_line)
                    current_line = word + " "
            lines_to_draw.append(current_line)

        # Calculate how many lines fit above the input box
        max_lines = (HEIGHT - 60) // (FONT_SIZE + 5)
        start_index = max(0, len(lines_to_draw) - max_lines)

        for line in lines_to_draw[start_index:]:
            text_surface = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(text_surface, (PADDING, y_offset))
            y_offset += FONT_SIZE + 5

    def draw(self):
        self.screen.fill(BG_COLOR)

        self.draw_text()

        # Input Box
        input_y = HEIGHT - 40
        pygame.draw.rect(self.screen, INPUT_BG_COLOR, (0, input_y, WIDTH, 40))
        input_surface = self.font.render(f"> {self.input_text}", True, INPUT_COLOR)
        self.screen.blit(input_surface, (PADDING, input_y + 10))

        if self.waiting_for_response:
             loading_surface = self.font.render("Thinking...", True, (255, 255, 0))
             self.screen.blit(loading_surface, (WIDTH - 150, input_y + 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.waiting_for_response:
                        self.handle_input(event)

            self.draw()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()
