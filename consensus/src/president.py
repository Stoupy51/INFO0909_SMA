
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
        """ Receive a message and process it """
        if message.origin == "Main":
            stp.debug(f"President Received message from '{message.origin}', content: '{str(message.content)[:25]}'")
        else:
            stp.info(f"President Received message from '{message.origin}', content: '{str(message.content)[:25]}'")

        dico_labels: dict[str, str] = {"0": "human", "1" : "AI"}

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
                    resultats = [0, 0]
                    for rep in self.responses.values():
                        resultats[int(rep)] += 1
                    maxi_index = str(resultats.index(max(resultats)))
                    stp.info(f"Voting finished, result: {resultats}, décision: {dico_labels[maxi_index]}")

                    

            # Si vote borda, on lance
            elif data_dict.get("request") == "borda":

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
                    # End voting
                    self.is_voting = False
                    resultats: list[int] = [0, 0]

                    # Initialize dictionary to store total points for each class
                    recap_points: dict[str, int] = {x: 0 for x in ["human", "ai"]}

                    # Process each agent's vote
                    for rep in self.responses.values():
                        # Split response into individual class-point pairs (removing trailing comma)                        
                        points: list[str] = rep[0:-1].split(',')
                        
                        # Extract and add points for first class
                        c1, p1 = points[0].split(' ')
                        recap_points[c1] += int(p1)
                        
                        # Extract and add points for second class
                        c2, p2 = points[1].split(' ')
                        recap_points[c2] += int(p2)

                    # Sort classes by total points in descending order
                    recap_points_sorted: list[tuple[str, int]] = sorted(recap_points.items(), key=lambda item: item[1], reverse=True)
                    
                    # Log final results
                    stp.info(f"Voting finished, result: {recap_points_sorted}")


            elif data_dict.get("request") == "paxos":
                pass


