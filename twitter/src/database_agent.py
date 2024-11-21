
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

class DatabaseAgent(Agent):
	class DatabaseBehaviour(CyclicBehaviour):

		async def on_start(self):
			""" Load the database """
			self.db: dict = {}
			if not DatabaseConfig.NEW_DATABASE_ON_START and os.path.exists(DatabaseConfig.FILE):
				with open(DatabaseConfig.FILE, "r") as f:
					self.db = json.load(f)
				info(f"Database loaded with {len(self.db)} tweets")
			self.send_to_models: bool = False

		async def run(self):
			""" Main agent behaviour, receive cleaned tweets and store them in the database """
			msg: Message|None = await self.receive(timeout=10)
			try:
				if msg:
					# Decode tweet
					json_dict: dict = json.loads(msg.body)
					tweet_id: str = json_dict.pop("id")

					# Store tweet in the database if id is not already present
					if not self.db.get(tweet_id):
						self.db[tweet_id] = json_dict
						self.save_db()
						self.send_to_models = True

				elif self.send_to_models:
					# Send updated database to SVM agent
					msg = Message(to=Agents.SVM[0])
					msg.body = json.dumps(self.db)
					await self.send(msg)
					self.send_to_models = False

			except Exception as e:
				error(f"Error with request from {msg.sender}: {e}", exit=False)
		
		def save_db(self):
			with open(DatabaseConfig.FILE, "w", encoding="utf-8") as f:
				json.dump(self.db, f, indent='\t')

	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.DatabaseBehaviour())
		pass



