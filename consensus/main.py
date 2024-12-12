
# Imports
from config import *
from src.agentTest import *
from autogen_core import SingleThreadedAgentRuntime


# Main function
@measure_time(progress)
@handle_error((KeyboardInterrupt,), error_log=0)
async def main():
	with SingleThreadedAgentRuntime() as runtime:
		runtime: SingleThreadedAgentRuntime

		agent = SimpleAgent()
		runtime.register_agent(agent)

		test_message = Message(content="Hello, Agent!")
		await agent.handle_message(test_message, None)



# Entry point of the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

