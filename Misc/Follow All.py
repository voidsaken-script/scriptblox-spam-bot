# this is optimizied to save all scripts from the same user to avoid having several 'already following user' problems, it also compensates for rate limits by retrying in 20s
# goes from most recent scripts and extracts the users profile to follow them with the api
token = "scriptblox token"

from scriptblox_api import Posts
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

page = 2
ignore = {}
modders = ["Hypernova", "ThunderMods", "galitsacheatertg", "Omsin", "Depso", "wyvern", "SoniSins", "batusd3009", "Arcturus", "Rauwo"]

while True:
	r = session.get("https://scriptblox.com/api/script/fetch?page=" + str(page))
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
		global uid
		uid = data['script']['owner']['_id']
		upage = 0
		while True:
			upage += 1
			userscripts = session.get("https://scriptblox.com/api/user/scripts/" + data['script']['owner']['username'] + "?page=" + str(upage))
			if userscripts.status_code == 429:
				sleep(10)
				upage -= 1
				continue
			userscripts = userscripts.json()
			if upage > userscripts['result']['totalPages']:
				break
			for uscript in userscripts['result']['scripts']:
				#print(f"{data['script']['owner']['username']}, {uscript['_id']}")
				ignore[uscript['_id']] = True
		if uid in ignore:
			#print("already following user")
			continue
		global udata
		udata = session.get(f"https://scriptblox.com/api/user/info/{uid}", headers={"authorization": token})
		if udata.status_code == 429:
			sleep(20)
			continue
		udata = udata.json()
		print(f"username: {data['script']['owner']['username']}\tid: {uid}")
		def tryFollow():
			if udata['user']['isFollowing']:
				#print("already following user")
				return
			pres = session.post("https://scriptblox.com/api/user/follow", headers={"authorization": token}, json={"userId": uid})
			if pres.status_code != 200:
				if pres.status_code != 429 and pres.json()['message'] == "You cannot follow yourself!":
					print("Skipped your own post")
					return
				print("rate limit (waiting 20s then retrying)")
				sleep(20)
				tryFollow()
			else:
				ignore[uid] = True
				print("Followed")
		tryFollow()
		sleep(3)
