
# Imports
import os
import sys

# Try to import every requirements
REQUIREMENTS: dict[str, str] = {
	"stouputils": None,
	"autogen_core": "autogen-core==0.4.0.dev11",
	"accelerate": None,
	"transformers": None,
	"torch": None,
}

exit_program: bool = False
for requirement, package_name in REQUIREMENTS.items():
	try:
		__import__(requirement)
	except ImportError:
		if package_name is None:
			package_name = requirement
		os.system(f"{sys.executable} -m pip install {package_name}")
		exit_program = True

# Exit program if any requirement has been installed
if exit_program:
	print("\nPlease restart the program.")
	sys.exit(-1)

