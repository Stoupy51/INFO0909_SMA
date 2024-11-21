
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from transformers import pipeline, Pipeline
import json

class LabellerAgent(Agent):
	class LabellerBehaviour(CyclicBehaviour):

		async def on_start(self):
			self.analyzer: Pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
	

		async def run(self):
			""" Main agent behaviour, receive cleaned tweets and store them in the database """
			msg: Message = await self.receive()
			try:
				if msg:
 					# Decode tweet
					json_dict: dict = json.loads(msg.body)
					content: str = json_dict["content"]

					# Analyze the content to get the label number
					analysis: dict = self.analyzer(content)[0]	# [{'label': '1 star', 'score': 0.9996980423927307}]
					label: str = analysis["label"]				# '1 star'
					label = label.split(' ')[0]					# '1 star' -> '1'

					# Get the sentiment out of the label
					json_dict["sentiment"] = LabellerConfig.LABELS[int(label)]

					# Send back to the database
					await self.send(Message(to=Agents.DATABASE[0], body=json.dumps(json_dict)))

			except Exception as e:
				error(f"Error with request from {msg.sender}: {e}", exit=False)


	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.LabellerBehaviour())
		pass


