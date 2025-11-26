# prints working tokens

from random import randint
from time import sleep
import tls_client

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

def get_tokens():
	#with open("bots.txt", "r") as f:
	with open("newbots.txt", "r") as f:
		return [token for token in f.read().splitlines()]

working = ""
for token in get_tokens():
    res = session.get("https://scriptblox.com/api/notification/fetch", headers={"authorization": token})
    if res.status_code != 200:
        continue
    res = res.json()
    try:
        if "notifications" in res:
            working += token + "\n"
    except:
        pass
print(working)
