# Gets scripts and comments on them
token = "Your scriptblox token"
message = "better skibidi simultator script here 50+ options and no key https://scriptblox.com/your-script"

from scriptblox_api import Posts, _createRealisticRequest
from time import sleep

import tls_client
from random import randint

chromeIdentifier = "chrome" + str(randint(112, 120))
session = tls_client.Session(
	client_identifier=chromeIdentifier,
	random_tls_extension_order=True,
	header_order=[
		"accept",
		"user-agent",
		"accept-encoding",
		"accept-language"
	]
)

page = 23
ignore = {}
modders = ["Hypernova", "ThunderMods", "galitsacheatertg", "Omsin", "Depso", "wyvern", "SoniSins", "batusd3009", "Arcturus", "Rauwo"]

while True:
	r = session.get("https://scriptblox.com/api/script/search?q=forsaken&page=" + str(page))
	if r.status_code == 429:
		print("rate limited when fetching scripts! Waiting 1 minute. do not interact w/ the site")
		sleep(60)
		continue
	r = r.json()
	result = r['result']
	page += 1
	if page > result['totalPages']:
		print("done and dusted.. out of this world!")
		break
	for script in result['scripts']:
		if script['_id'] in ignore:
			#print("skipped script")
			continue
		print(f"==== PAGE {page - 1} | {script['title']} ====")
		slugn = f"https://scriptblox.com/api/script/{script['slug']}"
		data = Posts.getScriptData(slugn)
		if data['script']['owner']['username'] in modders:
			print("SKIPPING ADMIN" + data['script']['owner']['username'] )
			continue
		if not data:
			sleep(20)
			continue
		def tryComment():
			json = {
				"scriptId": script['_id'],
				"text": message
			}
			pres = _createRealisticRequest("POST", url="https://scriptblox.com/api/comment/add", headers={"authorization": token}, json=json)
			if pres.status_code != 200:
				if pres.status_code != 429:
					print("Fatal error: " + str(pres.status_code))
					return
				print("rate limit (waiting 20s then retrying)")
				sleep(20)
				tryComment()
			else:
				print("Commented")
		tryComment()
		sleep(3)
