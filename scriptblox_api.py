import tls_client
import requests
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
	
def _createRealisticRequest(method, url, headers={}, json={}):
    headers["host"] = "scriptblox.com"
    headers["accept-encoding"] = "gzip, deflate, br, zstd"
    headers["referer"] = url
    headers["content-length"] = str(randint(39, 99))
    headers["origin"] = "https://scriptblox.com"
    headers["connection"] = "keep-alive"    
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
    headers["accept"] = "application/json"
    return requests.request(method, url, headers=headers, json=json)
