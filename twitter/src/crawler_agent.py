
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from twscrape import API, Tweet, gather
from typing import Iterable
import json

class CrawlerAgent(Agent):
	class CrawlerBehaviour(OneShotBehaviour):

		async def on_start(self):
			""" Setup the Twscrape API and connect the account """
			self.api = API()
			try:
				await self.api.pool.add_account(*CrawlerConfig.ACCOUNT)
				await self.api.pool.login_all()
				info("[Crawler] Logged in to Twitter")
			except Exception as e:
				error(f"Error while logging in to Twitter: {e}")

		async def run(self):
			""" Main agent behaviour, search for tweets """
			# Get the tweets
			tweets: Iterable[Tweet] = await gather(self.api.search(
				CrawlerConfig.QUERY,
				limit=CrawlerConfig.MAX_TWEETS
			))
			tweets = list(tweets)
			info(f"[Crawler] Scrapped {len(tweets)} tweets")

			# Send the tweets one by one
			for tweet in tweets:
				
				# Ask database if the tweet is already in database
				json_body: str = json.dumps({"id": tweet.id, "content": tweet.rawContent, "from_crawler": True})
				await self.send(Message(to=Agents.DATABASE[0], body=json_body))

				# If no, send it to the cleaner
				msg: Message|None = await self.receive(timeout=10)
				if msg and msg.body == "good":
					json_body: str = json.dumps({"id": tweet.id, "content": tweet.rawContent})
					await self.send(Message(to=Agents.CLEANER[0], body=json_body))
				else:
					warning(f"Tweet {tweet.id} already present")
				
				# Debug message
				#debug(f"[Crawler] Sent tweet {tweet.id} to {Agents.CLEANER[0]}")

	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.CrawlerBehaviour())
		pass



