import argparse
import sys
import os

# Ensure the root directory is in sys.path so we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def play(mode='smart', model_path='8500_Model4.pt', setup_only=False):
    try:
        import melee
        import time
        from src.constants_and_config.gconsants import DOLPHIN_PATH, ISO_PATH, DOLPHIN_HOME_PATH
        from src.bot.base_agent import BaseAgent
        from src.bot.smart_agent import SmartAgent
    except ImportError as e:
        print(f"Error importing dependencies: {e}")
        print("Make sure you have installed the requirements: pip install -r Files/requirements.txt")
        return

    print(f"Starting Dolphin from: {DOLPHIN_PATH}")
    print(f"Loading ISO from: {ISO_PATH}")
    print(f"Using Dolphin home path: {DOLPHIN_HOME_PATH}")

    # We use tmp_home_directory=False to use your live settings (keyboard/cheats)
    console = melee.console.Console(
        path=DOLPHIN_PATH,
        slippi_address="127.0.0.1",
        dolphin_home_path=DOLPHIN_HOME_PATH,
        tmp_home_directory=False,
    )
    
    # Port 2 is the Bot. Port 1 is YOUR KEYBOARD.
    # This allows you to use the keyboard on Port 1 to navigate if needed.
    controller_bot = melee.Controller(port=2, console=console)

    try:
        console.run(iso_path=ISO_PATH)
        print("Waiting for Dolphin to initialize (10 seconds)...")
        time.sleep(10)
        console.connect()

        print("Connecting Bot to Port 2...")
        controller_bot.connect()
        print("Connected successfully!")
    except Exception as e:
        print(f"Error starting Melee: {e}")
        return

    # Initialize Bot Agent on Port 2
    if mode == 'smart' and not setup_only:
        if not os.path.exists(model_path):
            print(f"Model file not found: {model_path}. Falling back to base mode.")
            agent = BaseAgent(controller_bot)
        else:
            agent = SmartAgent(controller_bot, modelPath=model_path)
    else:
        agent = BaseAgent(controller_bot)

    print(f"Running bot on Port 2 in {mode} mode... Press Ctrl+C to stop.")

    try:
        while True:
            gamestate = console.step()
            if gamestate is None:
                continue

            agent.set_gamestate(gamestate)

            if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
                if setup_only:
                    continue

                if mode == 'smart':
                    agent.move()
                else:
                    agent.random_act()
                    agent.random_tilt()
            else:
                # Automate menu navigation for the bot on Port 2
                # You can still use your keyboard on Port 1 to help it out!
                # We instantiate MenuHelper because it's an instance method in this version
                melee.menuhelper.MenuHelper().menu_helper_simple(gamestate, controller_bot,
                                                               melee.enums.Character.FOX,
                                                               melee.enums.Stage.FINAL_DESTINATION,
                                                               "", autostart=not setup_only, swag=True)
    except KeyboardInterrupt:
        print("\nStopping bot...")

def train():
    try:
        from src.training.train import run_training
        run_training()
    except ImportError as e:
        print(f"Error importing training logic: {e}")
    except Exception as e:
        print(f"An error occurred during training: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SmashBrosBot - Play or Train")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Play subparser
    play_parser = subparsers.add_parser("play", help="Run the bot to play the game")
    play_parser.add_argument("--mode", choices=["base", "smart"], default="smart", help="Bot mode (default: smart)")
    play_parser.add_argument("--model", default="8500_Model4.pt", help="Path to the model file for smart mode (default: 8500_Model4.pt)")
    play_parser.add_argument("--setup-only", action="store_true", help="Navigate to CSS and stop")

    # Train subparser
    train_parser = subparsers.add_parser("train", help="Train the AI model")

    args = parser.parse_args()

    if args.action == "play":
        play(mode=args.mode, model_path=args.model, setup_only=args.setup_only)
    elif args.action == "train":
        train()
    else:
        parser.print_help()
