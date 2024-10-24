
# Imports
from config import *
from src.crawler_agent import *
from src.cleaner_agent import *
from src.labeller_agent import *
from src.database_agent import *
from spade import wait_until_finished, run as spade_run
from spade.agent import Agent

# Main function
async def main():

	# Print the start time
	info(f"Start time: {START_TIME_STR}")

	# Create all the agents and start them.
	instances: list[Agent] = [
		CrawlerAgent(*Agents.CRAWLER),
		CleanerAgent(*Agents.CLEANER),
		LabellerAgent(*Agents.LABELLER),
		DatabaseAgent(*Agents.DATABASE),
	][::-1]
	
	for instance in instances:
		await instance.start()
		debug(f"Agent {instance.name} started")

	# Wait until the agents are finished
	warning("Wait until user interrupts with CTRL+C")
	await wait_until_finished(instances)

	# End of the script
	info("End of the script")
	return



# Entry point of the script
if __name__ == "__main__":
	spade_run(main())

