
## Configuration file for the application
from src.requirements import *
from src.print import *
from dataclasses import dataclass
import json
import os

# Constants for start time
START_TIME: float = time.time()
START_TIME_STR: str = time.strftime("%Y-%m-%d %H:%M:%S")

# Folders
ROOT: str = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")	# Root folder (where the config.py file is located)
DATASET: str = f"{ROOT}/updated_pollution_dataset.xls"

@dataclass
class Message:
	content: str = ""
	data: str = "{}"
	origin: str = ""

