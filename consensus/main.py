
# Imports
from config import *
from src.president import *
from src.Ollama import *
from src.BERT import *
from autogen_core import SingleThreadedAgentRuntime, AgentId
from typing import Type
import pandas as pd
import stouputils as stp

async def register_agent(runtime, agent_class: Type[BaseAgent]):
    await agent_class.register(runtime, agent_class.__name__, lambda: agent_class())

# Main function
@stp.handle_error(KeyboardInterrupt, error_log=0)
async def main():
	runtime = SingleThreadedAgentRuntime()
	await register_agent(runtime, PresidentAgent)
	await register_agent(runtime, Ollama)
	await register_agent(runtime, Bert)
	agents: list[str] = ["Ollama", "Bert"]
	
	runtime.start()
	await runtime.send_message(Message("start", data=json.dumps(agents)), AgentId("PresidentAgent", "default"))

	# Vote majoritaire
	pass

	# le Borda
	pass

	# PAXOS
	pass

	await runtime.stop()
	return



# Entry point of the script
if __name__ == "__main__":
	import asyncio
	asyncio.run(main())

