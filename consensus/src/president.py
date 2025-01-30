
# Imports
from config import *
from autogen_core import MessageContext, BaseAgent, AgentId
import stouputils as stp
import pandas as pd

# Class
class PresidentAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        self.propositions: list = []
        self.agents: list[str] = []
        self.msg: Message = Message(origin=self.__class__.__name__)

    async def on_message_impl(self, message: Message, ctx: MessageContext) -> None:
        stp.info(f"President Received message: {message.content}")
        data: list|dict = json.loads(message.data)

        if message.content == "start":
            self.agents = data
            stp.debug(self.agents)
 
            # Load dataset
            self.dataset = pd.read_csv(DATASET)

            # Envoie du premier prompt
            self.msg.content = self.dataset.iloc[0][0]
            for agt in self.agents:
                await self.send_message(self.msg, AgentId(agt, "default"))
        else:
            data = json.loads(message.data)
            if data.get("request") == "":
                pass


