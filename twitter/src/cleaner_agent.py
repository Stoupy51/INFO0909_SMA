
# Imports
from config import *
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from nltk.corpus import stopwords
import string
import nltk
import json


class CleanerAgent(Agent):
	class CleanerBehaviour(CyclicBehaviour):
		async def on_start(self):
			nltk.download('stopwords')
			info("[Cleaner] Successfully started")

		async def run(self):
			""" Run method. Cleans the tweets and sends them to the database """
			msg: Message = await self.receive(timeout=60)

			if msg:
				# Si on reçoit un tweet -> on récupère le text
				json_dict: dict = json.loads(msg.body)
				content: str = json_dict["content"]
				content = content.strip()
				
				# On enlève les liens
				if CleanerConfig.REMOVE_LINKS:
					content = " ".join([word for word in content.split() if not word.startswith("http")])

				# On enlève la ponctuation
				if not CleanerConfig.KEEP_SPECIAL_CHARS:
					for p in string.punctuation:
						content = content.replace(p, " ")

				# On enlève les doubles espaces
				while "  " in content:
					content = content.replace("  ", " ")
				
				# On enlève les accents
				if CleanerConfig.REMOVE_ACCENTS:
					content = content.encode("ascii", "ignore").decode("ascii")

				# On met les mots en minuscule
				if CleanerConfig.LOWER_CASE:
					content = content.lower()

				# On enlève les stop words
				if CleanerConfig.STOPWORDS:
					stop_words = set(stopwords.words("french"))
					content = " ".join(word for word in content.split(' ') if word not in stop_words)
				json_dict["content"] = content.strip()
				
				# Envoyer le message à la database
				await self.send(Message(to=Agents.LABELLER[0], body=json.dumps(json_dict)))
			pass

	async def setup(self):
		""" Agent initialization """
		self.add_behaviour(self.CleanerBehaviour())
		


