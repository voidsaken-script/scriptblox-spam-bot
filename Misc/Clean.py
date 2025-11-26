# write all working tokens to a file

def get_tokens():
	#with open("bots.txt", "r") as f:
	with open("newbots.txt", "r") as f:
		return [token for token in f.read().splitlines()]
	
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
	
cleaned = ""
for token in get_tokens():
	res = session.get("https://scriptblox.com/api/notification/fetch", headers={"authorization": token})
	if res.status_code == 200:
		cleaned += token + "\n"
		
open("cleanedbots.txt", "w").write(cleaned)
