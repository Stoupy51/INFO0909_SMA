
# Imports
from config import *
from src.president import *
from src.SVM import *
from src.randomForest import *
from src.gaussianNB import *
from autogen_core import SingleThreadedAgentRuntime, AgentId
import pandas as pd

# Main function
@measure_time(progress)
@handle_error((KeyboardInterrupt,), error_log=0)
async def main():
	runtime = SingleThreadedAgentRuntime()
	await PresidentAgent.register(runtime, "President", lambda: PresidentAgent())
	await SVMAgent.register(runtime, "SVM", lambda: SVMAgent())
	await RFAgent.register(runtime, "RandomForest", lambda: RFAgent())
	await NBAgent.register(runtime, "GaussianNB", lambda: NBAgent())
	agents: list[str] = ["SVM", "RandomForest", "GaussianNB"]
	
	runtime.start()

	test_message = Message(content="Hello, Agent!", data=json.dumps({"request":"Hello, Agent!"}))
	await runtime.send_message(test_message, AgentId("SVM", "default"))
	await runtime.send_message(test_message, AgentId("RandomForest", "default"))
	await runtime.send_message(test_message, AgentId("GaussianNB", "default"))

	await runtime.send_message(Message("start", data=json.dumps(agents)), AgentId("President", "default"))

	await runtime.stop()
	return



# Entry point of the script
if __name__ == "__main__":
	import asyncio
	asyncio.run(main())

