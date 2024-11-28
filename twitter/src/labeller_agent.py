
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from transformers import pipeline, Pipeline
import json
import requests

class LabellerAgent(Agent):
	class LabellerBehaviour(CyclicBehaviour):

		async def on_start(self):
			#self.analyzer: Pipeline = pipeline("sentiment-analysis", model="ac0hik/Sentiment_Analysis_French")
			pass

		async def run(self):
			""" Main agent behaviour, receive cleaned tweets and store them in the database """
			msg: Message = await self.receive()
			try:
				if msg:
 					# Decode tweet
					json_dict: dict = json.loads(msg.body)
					content: str = json_dict["content"]

					# Analyze the content to get the label number
					# analysis: dict = self.analyzer(content)	# [{'label': 'negative', 'score': 0.9996980423927307}]
					# #debug(f"Analysis: {analysis}")
					# label: str = analysis[0]["label"]		# 'negative'

					# Analyze the content with API
					data: dict = {
						"model": LabellerConfig.MODEL,
						"prompt": LabellerConfig.PROMPT.replace("REPLACE", content),
						"stream": False
					}

					# Faire la requête POST
					response = requests.post(LabellerConfig.API_URL, json=data)

					# Vérifier la réponse
					if response.status_code == 200:
						response_data = response.json()
						label = response_data["response"].lower()
						label = "".join(x for x in label if x in "abcedfghijklmnopqrstuvwxyz")
						suggestion(f"Response: {label}")
						if label not in LabellerConfig.LABELS:
							error(f"Response: {label}", exit=False)
							label = LabellerConfig.LABELS["neutral"]
					else:
						error(f"Erreur lors de la requête : {response.status_code}, {response.text}")

					# Get the sentiment out of the label
					json_dict["sentiment"] = LabellerConfig.LABELS[label]

					# Send back to the database
					await self.send(Message(to=Agents.DATABASE[0], body=json.dumps(json_dict)))

			except Exception as e:
				error(f"Error with request from {msg.sender}: {e}", exit=False)


	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.LabellerBehaviour())
		pass


