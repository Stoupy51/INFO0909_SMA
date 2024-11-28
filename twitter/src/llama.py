# Imports
from src.print import *
from config import *
import os
import requests

# Constants
GITHUB_LINK: str = "https://github.com/ollama/ollama"

# Blocking function that start ollama in background (should be started by a thread)
def background_llama() -> None:
    try:
        requests.get(LabellerConfig.API_URL)
    except requests.exceptions.RequestException:
        # API is not responding, open the browser to download the application
        os.system(f"start {GITHUB_LINK}")
        error(f"'ollama' application not found, please download from: '{GITHUB_LINK}'", exit=False)

