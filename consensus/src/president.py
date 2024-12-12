
# Imports
from config import *
from src.print import *
from autogen_core import MessageContext, BaseAgent, AgentId
import pandas as pd


class PresidentAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("PresidentAgent")
        self.propositions: list = []
        self.agents: list[str] = []
        self.msg: Message = Message(origin="President")

    async def on_message_impl(self, message: Message, ctx: MessageContext) -> None:
        info(f"President Received message: {message.content}")
        data: list|dict = json.loads(message.data)

        if message.content == "start":
            self.agents = data
            debug(self.agents)
            self.msg.content = "Je suis votre président"
            for agt in self.agents:
                await self.send_message(self.msg, AgentId(agt, "default"))
 
            # Load dataset
            self.dataset = pd.read_csv(DATASET)

            # Envoie de la première ligne (features)
            first_line = self.dataset.iloc[0][:-1]
            self.msg.content = ""
            self.msg.data = json.dumps(first_line)
            for agt in self.agents:
                await self.send_message(self.msg, AgentId(agt, "default"))
        else:
            pass


            data = json.loads(message.data)
            if data.get("request") == "":
                pass
