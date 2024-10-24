
# Imports
from config import *
from src.print import *
from src.crawler_agent import *
from src.cleaning_agent import *
from spade import wait_until_finished, run as spade_run
from spade.agent import Agent

# Main function
def main():

	# Print the start time
	info(f"Start time: {START_TIME_STR}")

	# Create all the agents and start them.
	instances: list[Agent] = [
		CrawlerAgent(*Agents.CRAWLER),
		#CleanerAgent(*Agents.CLEANER),
		#DatabaseAgent(*Agents.DATABASE),
	]
	for instance in instances:
		instance.start()

	# Wait until the agents are finished
	warning("Wait until user interrupts with CTRL+C")
	wait_until_finished(*instances)

	# End of the script
	info("End of the script")
	return



# Entry point of the script
if __name__ == "__main__":
	spade_run(main())

