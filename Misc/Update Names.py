# update names of the bots if they get leaked

import time
import tls_client
from random import randint, choice
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
	
def generate_hex_name():
    hex_chars = '0123456789abcdef'
    return ''.join(choice(hex_chars) for _ in range(20))

if True:
    for token in get_tokens():
        r = session.post("https://scriptblox.com/api/user/update", headers={"authorization": token}, json={"bio": "No bio provided.", "username": generate_hex_name()})
        print(r.status_code)
        print(r.json())
        time.sleep(2)
