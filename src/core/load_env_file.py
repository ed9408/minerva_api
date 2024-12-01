import os

from pathlib import Path


def load_env_file(file_name: str = ".env") -> None:
    """Load environment variables from a file.

    Parameters:
        file_name (str): The name of the dot env file.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env_file = BASE_DIR / file_name

    try:
        with open(env_file, "r") as f:
            for line in f.readlines():
                config_line = line.strip()

                if config_line.startswith("#"):
                    continue

                key, value = config_line.split("=")
                os.environ[key] = value
    except FileNotFoundError:
        pass
