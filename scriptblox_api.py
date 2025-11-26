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

class Posts:
	def getScriptData(link):
		res = session.get(link)
		if res.status_code != 200:
			return False
		return res.json()
