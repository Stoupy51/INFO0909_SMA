
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class CleaningAgent(Agent):
	class CleaningBehaviour(OneShotBehaviour):
		async def on_start(self):
			"""
			"""
			pass
		async def run(self):
			"""
			"""
			msg: Message = await self.receive()
			if msg:
				#si on reçoit un tweet -> n récupèrel'id et le text
				id_t, text_t = msg.body.split(',',1)
				
				if not CleanerConfig.KEEP_SPECIAL_CHARS:
					#on enlève les caractères spéciaux
				
				

 	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.CrawlerBehaviour())
		pass


			