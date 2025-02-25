
# Imports
from config import *
from typing import Any
from autogen_core import MessageContext, BaseAgent, AgentId
import stouputils as stp
import json

# Class
class PresidentAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        self.propositions: list = []
        self.agents: list[str] = []
        self.msg: Message = Message(origin=self.__class__.__name__)
        self.is_voting: bool = False
        self.responses: dict[str, Any] = {}

    async def on_message_impl(self, message: Message, ctx: MessageContext) -> None:
        stp.info(f"President Received message from '{message.origin}', content: '{str(message.content)[:25]}'")

        # Si c'est une réponse, on enregistre
        if message.origin in self.agents:
            self.responses[message.origin] = message.content

        # Sinon, message de la fonction main
        elif message.content == "register":
            data_list: list = json.loads(message.data)
            self.agents += data_list
        else:
            data_dict: dict = json.loads(message.data)
            # Si vote majoritaire, on lance
            if data_dict.get("request") == "majoritaire":

                # Si le vote n'est pas démarré, on envoie à tout le monde
                if not self.is_voting:
                    self.is_voting = True

                    # On prépare la liste des réponses
                    self.responses = {x: None for x in self.agents}

                    # On envoie à tous
                    self.msg.content = message.content
                    self.msg.data = message.data
                    for agt in self.agents:
                        await self.send_message(self.msg, AgentId(agt, "default"))
                
                # Si le vote est démarré, on l'arrête et on décide.
                else:
                    self.is_voting = False

                    

            elif data_dict.get("request") == "borda":
                pass

            elif data_dict.get("request") == "paxos":
                pass


