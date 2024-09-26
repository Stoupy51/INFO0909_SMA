
# Imports
from config import *
import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class CrawlerAgent(Agent):
	class CrawlerBehaviour(OneShotBehaviour):

		async def on_start(self):
			""" Setup the agent variables such as remaining tasks """
			self.remaining_tasks: int = CrawlerConfig.MAX_TWEETS

		async def run(self):
			""" Main agent behaviour, search for tweets """
			# TODO: Implement the search for tweets
			while self.remaining_tasks > 0:
				self.remaining_tasks -= 1
				pass
			pass

	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.CrawlerBehaviour())
		pass



