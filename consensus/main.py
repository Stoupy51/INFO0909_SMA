
# Imports
from config import *
from src.president import *
from src.Ollama import *
from src.BERT import *
from src.AgentRandom import *
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
	await register_agent(runtime, AgentRandom)
	# await register_agent(runtime, Bert)
	agents: list[str] = ["Ollama", "AgentRandom"]#, "Bert"]
	
	runtime.start()
	presi = AgentId("PresidentAgent", "default")
	await runtime.send_message(Message("register", data=json.dumps(agents)), presi)

	# Load dataset
	dataset = pd.read_csv(DATASET)
	text = dataset.iloc[0][0]

	# Vote majoritaire
	stp.progress("Lancement du vote majoritaire")
	await runtime.send_message(Message(text, data='{"request":"majoritaire"}'), presi)
	await runtime.send_message(Message("fin", data='{"request":"majoritaire"}'), presi)

	# le Borda
	stp.progress("Lancement du vote Borda")
	await runtime.send_message(Message(text, data='{"request":"borda"}'), presi)
	await runtime.send_message(Message("fin", data='{"request":"borda"}'), presi)

	# PAXOS
	stp.progress("Lancement du vote PAXOS")
	await runtime.send_message(Message(text, data='{"request":"paxos"}'), presi)
	await runtime.send_message(Message("fin", data='{"request":"paxos"}'), presi)

	await runtime.stop()
	return



# Entry point of the script
if __name__ == "__main__":
	import asyncio
	asyncio.run(main())

