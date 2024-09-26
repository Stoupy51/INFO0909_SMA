
# Imports
import asyncio
import time
import random
import spade
from spade import wait_until_finished
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message

JUGE = "zahia_guess@pwned.life"
JOUEUR_1 = "Stoupy51@pwned.life"
JOUEUR_2 = "agent801@pwned.life"
JOUEUR_2_PWD = "cours801"

AGENTS: dict = {
	"zahia_guess@pwned.life":	"zahia",
	"Stoupy51@pwned.life":		"uwu",
	"agent801@pwned.life":		"cours801",
}

class JoueurAgent(Agent):
	class JoueurBehaviour(CyclicBehaviour):
		
		async def on_start(self):
			pass

		async def run(self):
			msg = await self.receive(timeout = 60)
			if msg:
				try:
					is_value = int(msg.body)
					time.sleep(1)
					print(f"[{self.name}] somme reçu de {msg.body}")
					r = random.randint(1, 3)
					print(f"[{self.name}] joueur joue : {r}")
					await self.send(Message(to = JUGE, body = f"{r}"))
				except ValueError:
					print(f"[{self.name}] Fin de la partie, message reçu : {msg.body}")
					self.kill()
				

	async def setup(self):
		print("JoueurAgent starting . . .")
		b = self.JoueurBehaviour()
		b.name = self.jid
		self.add_behaviour(b)



class JugeAgent(Agent):
	class JugeBehaviour(OneShotBehaviour):
		
		async def on_start(self):
			self.turn = random.randint(0, 1)
			self.somme = 0
			if self.turn == 0:
				print("Joueur 1 commence, envoie du message")
				await self.send(Message(to = JOUEUR_1, body = f"{self.somme}"))
			else:
				print("Joueur 2 commence, envoie du message")
				await self.send(Message(to = JOUEUR_2, body = f"{self.somme}"))
		
		async def run(self):
			# Wait for an answer
			running = True
			MAX_VALUE = 21
			while running:
				msg = await self.receive(timeout = 60)
				if msg:
					self.somme += int(msg.body)
					if self.turn == 0:
						print(f"Joueur 1 a joué, somme = {self.somme}")
						if self.somme < MAX_VALUE:
							await self.send(Message(to = JOUEUR_2, body = f"{self.somme}"))
					else:
						print(f"Joueur 2 a joué, somme = {self.somme}")
						if self.somme < MAX_VALUE:
							await self.send(Message(to = JOUEUR_1, body = f"{self.somme}"))
					self.turn = 1 - self.turn
					if self.somme >= MAX_VALUE:
						running = False
						message = f"Joueur {self.turn + 1} a gagné !" if self.somme == MAX_VALUE else f"Joueur {self.turn + 1} a perdu !"
						print(message)
						await self.send(Message(to = JOUEUR_1, body = message))
						await self.send(Message(to = JOUEUR_2, body = message))
						running = False
			self.kill()
			return None


	async def setup(self):
		""" Création des joueurs """
		print("JugeAgent starting . . .")
		self.joueur_1 = JoueurAgent(JOUEUR_1, "uwu64")
		self.joueur_2 = JoueurAgent(JOUEUR_2, JOUEUR_2_PWD)
		await self.joueur_1.start()
		await self.joueur_2.start()
		self.add_behaviour(self.JugeBehaviour())








# Main function
async def main():
	
	# Create the Agent and start it
	juge = JugeAgent("zahia_guess@pwned.life", "zahia")
	await juge.start()

	# Wait until the agent is finished
	print("Wait until user interrupts with CTRL+C")
	await wait_until_finished(juge)

if __name__ == "__main__":
	spade.run(main())

