
## Configuration file for the application
from src.requirements import *
from src.print import *
from dataclasses import dataclass
import json
import os

# Folders
ROOT: str = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")	# Root folder (where the config.py file is located)
DATASET: str = f"{ROOT}/AI_Human.csv"

@dataclass
class Message:
	content: str = ""
	data: str = "{}"
	origin: str = ""

