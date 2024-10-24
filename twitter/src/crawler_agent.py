
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from twscrape import API, Tweet, gather
from typing import Iterable


class CrawlerAgent(Agent):
	class CrawlerBehaviour(OneShotBehaviour):

		async def on_start(self):
			""" Setup the Twscrape API and connect the account """
			self.api = API()
			await self.api.pool.add_account(*CrawlerConfig.ACCOUNT)
			await self.api.pool.login_all()

		async def run(self):
			""" Main agent behaviour, search for tweets """
			# Get the tweets
			tweets: Iterable[Tweet] = await gather(self.api.search(CrawlerConfig.QUERY, limit=CrawlerConfig.MAX_TWEETS))

			# Send the tweets one by one
			for tweet in tweets:
				await self.send(Message(to = Agents.CLEANER, body = f"{tweet.id},{tweet.rawContent}"))


	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.CrawlerBehaviour())
		pass



