
## Configuration file for the application
from src.requirements import *
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
	LANG: str = "fr"					# Language

# Cleaner config
class CleanerConfig():
	KEEP_SPECIAL_CHARS: bool = False	# Keep special characters
	LOWER_CASE: bool = True				# Apply lower case
	STOPWORDS: bool = True				# Remove stopwords


# Spade config
AGENTS: dict[tuple[str,str]] = {
	"crawler":	("zahia_guess@pwned.life",	"zahia"),
	"cleaner":	("Stoupy51@pwned.life",		"uwu"),
	"database":	("agent801@pwned.life",		"cours801"),
	"labeller":	(None, None),
}
class Agents():
	CRAWLER: tuple[str,str] =	("zahia_guess@pwned.life",	"zahia")
	CLEANER: tuple[str,str] =	("Stoupy51@pwned.life",		"uwu")
	DATABASE: tuple[str,str] =	("agent801@pwned.life",		"cours801")
	LABELLER: tuple[str,str] =	(None, None)

