
import asyncio
import csv
import json
from twscrape import API, Tweet, gather
from typing import Iterable

ACCOUNT: list = ["info0909sma", "impossible51", "info0909sma@gmail.com", "impossible51"]
#COOKIES: str = 'des_opt_in=Y; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A172734628802366282; guest_id_marketing=v1%3A172734628802366282; _ga=GA1.2.799828170.1727347062; lang=en; dnt=1; guest_id=v1%3A172916073514043431; gt=1846860098590683460; g_state={"i_p":1729247183073,"i_l":2}; twid=u%3D1846859152121077760; ct0=bbfce717a42192e58c6fecfc578817bc44a18518d5f4f326818c2ff05bfb1265a0922dfc162ea22081ccacd4c5bcd0aa047cfe71d163919dd4d4b0e46b811d9a94f4934e36f2338c20e5bd806fa2a048; personalization_id="v1_/5SfloXGjjeTQo83g1cmZw=="; {1c992ed0-bc81-4b30-bb10-651aa1cc7bf8}=value; night_mode=2'
QUERY: str = "gouvernement Barnier"
LIMIT: int = 100

async def fetch_tweets(api: API, query: str, limit: int = 1):
	tweets: Iterable[Tweet] = await gather(api.search(query, limit=limit))
	return await gather(api.search(query, limit=limit))

# Fonction principale pour récupérer et sauvegarder les tweets
async def main():

	# Initialiser l'API
	api = API()
	await api.pool.add_account(*ACCOUNT)#, cookies = COOKIES)
	await api.pool.login_all()

	# Récupérer les tweets
	tweets = await fetch_tweets(api, QUERY)#, LIMIT)

	# print the firt tweet (id and rawContent)
	print(tweets[0].id)
	print(tweets[0].rawContent)

# Lancer le script
if __name__ == "__main__":
	asyncio.run(main())

