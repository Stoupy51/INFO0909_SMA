
## Configuration file for the application
from src.requirements import *
from src.print import *
import os

# Constants for start time
START_TIME: float = time.time()
START_TIME_STR: str = time.strftime("%Y-%m-%d %H:%M:%S")

# Folders
ROOT: str = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")	# Root folder (where the config.py file is located)
DATASET: str = f"{ROOT}/dataset"

@dataclass
class Message:
    content: str

# SVM config
class SVMConfig():
	MAX_FEATURES: int = 1000        # Maximum number of features for TF-IDF
	KERNEL: str = 'linear'          # Kernel type ('linear', 'rbf', 'poly', 'sigmoid')
	TEST_SIZE: float = 1/3          # Test set size for train/test split
	RANDOM_STATE: int = 42          # Random state for reproducibility

