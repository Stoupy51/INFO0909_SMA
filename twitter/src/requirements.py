
# Imports
import os
import sys

# Try to import every requirements
REQUIREMENTS: list[str] = ["requests", "spade", "twscrape", "nltk", "transformers", "sklearn"]
EXIT_PROGRAM: bool = False
for requirement in REQUIREMENTS:
	try:
		__import__(requirement)
	except ImportError:
		if requirement == "sklearn":
			os.system(f"{sys.executable} -m pip install scikit-learn")
		else:
			os.system(f"{sys.executable} -m pip install {requirement}")
		EXIT_PROGRAM = True

# Exit program if any requirement has been installed
if EXIT_PROGRAM:
	print("Please restart the program.")
	sys.exit(-1)

