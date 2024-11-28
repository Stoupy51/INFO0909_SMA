
## Configuration file for the application
from src.requirements import *
from src.print import *
import time
import os

# Constants for start time
START_TIME: float = time.time()
START_TIME_STR: str = time.strftime("%Y-%m-%d %H:%M:%S")

# Folders
ROOT: str = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")	# Root folder (where the config.py file is located)

# Crawler config
class CrawlerConfig():
	ACCOUNT: list = ["info0909sma", "impossible51", "info0909sma@gmail.com", "impossible51"]
	MAX_TWEETS: int = 1					# Maximum number of tweets for an agent	
	QUERY: str = "gouvernement barnier"	# Query to search

# Cleaner config
class CleanerConfig():
	REMOVE_LINKS: bool = True			# Remove links
	KEEP_SPECIAL_CHARS: bool = False	# Keep special characters
	REMOVE_ACCENTS: bool = True			# Remove accents
	LOWER_CASE: bool = True				# Apply lower case
	STOPWORDS: bool = False				# Remove stopwords

# Labeller config
class LabellerConfig():
	LABELS: dict[str, str] = {
		"negative":	"Negatif",
		"neutral":	"Neutre",
		"positive":	"Positif"
	}
	API_URL: str = "http://localhost:11434/api/generate"
	MODEL: str = "llama3.2"	# https://ollama.com/download/OllamaSetup.exe
	PROMPT: str = """
Voici une phrase :
"REPLACE"

Répond juste "positive" si la phrase est positive, "negative" si elle est négative, "neutral" dans le cas contraire.
SEULEMENT CES MOTS !
"""

# SVM config
class SVMConfig():
	MAX_FEATURES: int = 1000        # Maximum number of features for TF-IDF
	KERNEL: str = 'linear'          # Kernel type ('linear', 'rbf', 'poly', 'sigmoid')
	TEST_SIZE: float = 1/3          # Test set size for train/test split
	RANDOM_STATE: int = 42          # Random state for reproducibility

# Database config
class DatabaseConfig():
	NEW_DATABASE_ON_START: bool = False	# Create a new database on start
	FILE: str = f"{ROOT}/database.json"	# Database file

# Spade config
class Agents():
	CRAWLER: tuple[str,str] =	("zahia_guess@pwned.life",	"zahia")
	CLEANER: tuple[str,str] =	("Stoupy51@pwned.life",		"uwu64")
	DATABASE: tuple[str,str] =	("agent801@pwned.life",		"cours801")
	LABELLER: tuple[str,str] =	("label@pwned.life", 		"label")
	SVM: tuple[str,str] =		("svm123@pwned.life",		"svm123")

