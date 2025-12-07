# Gemini AD&D 2nd Edition Interactive Fiction

This is a Pygame-based interactive fiction game engine powered by Google Gemini AI, designed to run Advanced Dungeons & Dragons 2nd Edition campaigns.

## Prerequisites

- Python 3.8+
- A Google Gemini API Key

## Setup

1.  **Clone the repository.**
2.  **Run the setup script:**

    *   **Linux/macOS:**
        ```bash
        ./setup.sh
        ```
    *   **Windows:**
        ```cmd
        setup.bat
        ```

3.  **Configure API Key:**

    Create a file named `.env` in the root directory and add your Google Gemini API key:

    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

    You can get an API key from [Google AI Studio](https://aistudio.google.com/).

## Running the Game

Once setup is complete and the `.env` file is created, run the game using:

*   **Linux/macOS:**
    ```bash
    ./run.sh
    ```
*   **Windows:**
    ```cmd
    run.bat
    ```

## How it Works

- **`src/main.py`**: The entry point of the application.
- **`src/game.py`**: Handles the Pygame window, rendering text, and capturing user input.
- **`src/gemini_dm.py`**: Manages the connection to Google Gemini, sending the prompt context (AD&D 2nd Ed rules) and user actions.
- **`src/config.py`**: Loads environment variables.

## Controls

- **Typing**: Type your actions into the input box at the bottom.
- **Enter**: Send your action to the Gemini Dungeon Master.
- **Backspace**: Edit your input.

### Commands

The following commands are handled locally by the game engine and are **not** sent to the DM AI:

- **`exit`**: Closes the game.
- **`save`**: Saves the current game state to `savegame.json`.
- **`load`**: Loads the game state from `savegame.json`.
- **`supervise`**: Issues a system instruction to the AI to correct deviations or hallucinations.

All other text input is sent to the Gemini AI to be processed as part of the game.

## Customization

You can modify the system prompt in `src/gemini_dm.py` to change the tone, setting, or specific rules of the campaign.
