import os
import subprocess
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

RUN_SCRIPT = PROJECT_ROOT / "scripts" / "run.sh"

VENV_DIR = PROJECT_ROOT / ".venv"

VENV_PYTHON = VENV_DIR / "bin" / "python"

VENV_STREAMLIT = VENV_DIR / "bin" / "streamlit"


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

def setup_environment() -> None:
    """
    Run the project environment setup script.
    """

    subprocess.run(
        [
            "bash",
            str(RUN_SCRIPT),
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )


def get_environment() -> dict[str, str]:
    """
    Return the environment used by the application.
    """

    environment = os.environ.copy()

    environment["PYTHONPATH"] = str(
        PROJECT_ROOT / "src"
    )

    return environment


# ---------------------------------------------------------
# Web UI
# ---------------------------------------------------------

def start_web_ui() -> None:
    """
    Start the Streamlit web interface
    using the project virtual environment.
    """

    subprocess.run(
        [
            str(VENV_STREAMLIT),
            "run",
            "app/app.py",
        ],
        check=False,
        cwd=PROJECT_ROOT,
        env=get_environment(),
    )


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def start_cli() -> None:
    """
    Start the command-line interface.
    """

    environment = get_environment()

    subprocess.run(
        [
            str(VENV_PYTHON),
            "-c",
            (
                "from app.cli import main; "
                "main()"
            ),
        ],
        check=False,
        cwd=PROJECT_ROOT,
        env=environment,
    )


# ---------------------------------------------------------
# Menu
# ---------------------------------------------------------

def show_menu() -> None:
    """
    Display the interface selection menu.
    """

    print("=" * 60)
    print("Voltix Project Chatbot")
    print("=" * 60)
    print()
    print("Choose an interface:")
    print()
    print("1. Web UI")
    print("2. CLI")
    print("0. Exit")
    print()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main() -> None:
    """
    Start the Voltix chatbot.
    """

    setup_environment()

    while True:

        show_menu()

        choice = input("Select an option: ").strip()

        if choice == "1":

            print()
            print("Starting Web UI...")
            print()

            start_web_ui()

            break

        elif choice == "2":

            print()
            print("Starting CLI...")
            print()

            start_cli()

            break

        elif choice in {"0", "exit", "quit"}:

            print()
            print("Goodbye!")

            break

        else:

            print()
            print(
                "Invalid option. "
                "Please choose 1, 2, or 0."
            )
            print()


if __name__ == "__main__":
    main()