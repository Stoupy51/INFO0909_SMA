
## Configuration file for the application
from src.requirements import *
from dataclasses import dataclass
import os

# Folders
ROOT: str = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")	# Root folder (where the config.py file is located)
DATASET: str = f"{ROOT}/dataset.csv"

@dataclass
class Message:
	content: str = ""
	data: str = "{}"
	origin: str = ""

