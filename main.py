# I am posting this on github because this tool does NOT work anymore!

from scriptblox_api import *
from dotenv import load_dotenv
from os import getenv
from discord.ext import commands
from random import randint, choice
from time import sleep, time
import re
import discord
import tls_client
import requests
import json as jsonUtil

chromeIdentifier = "chrome" + str(randint(112, 120))
session = tls_client.Session(
	client_identifier=chromeIdentifier,
	random_tls_extension_order=True,
	header_order=[
		"Accept",
		"Accept-Encoding",
		"Accept-Language",
		"Alt-Used",
		"Connection",
		"Host",
		"Priority",
		"Referer",
		"Sec-Fetch-Dest",
		"Sec-Fetch-Mobile",
		"Sec-Fetch-Mode",
		"Sec-Fetch-Site",
		"TE",
		"User-Agent",
	],
)
pro = None # if you got a proxy, set it here

load_dotenv()
token = getenv("TOKEN")

# tokens
def get_tokens():
	#with open("bots.txt", "r") as f:
	with open("newbots.txt", "r") as f:
		return [token for token in f.read().splitlines()]

# embed
def makeInfoEmbed(id, creator, scriptData, title, verified, color):
	infoEmbed = discord.Embed(title=title, color=color)
	infoEmbed.set_footer(text="Scriptbot V2 [sabotaged by reactor twice]")
	infoEmbed.add_field(name="Views", value=str(scriptData['views']))
	infoEmbed.add_field(name="Likes", value=str(scriptData['likeCount']))
	infoEmbed.add_field(name="Haters", value=str(scriptData['dislikeCount']))
	infoEmbed.add_field(name="ID", value=id)
	infoEmbed.add_field(name="Creator", value=f"{creator} {verified and ":white_check_mark:" or ""}")
	infoEmbed.add_field(name="Game", value=scriptData['game']['name'])
	return infoEmbed
def makeAdvancedInfoEmbed(id, creator, scriptData, title, verified, color):
	created = re.search(r"(\d\d\d\d-\d\d-\d\d)", scriptData['createdAt']).group(1)
	infoEmbed = discord.Embed(title=title, color=color)
	infoEmbed.set_footer(text="Scriptbot V2 [sabotaged by reactor]")
	infoEmbed.add_field(name="Views", value=str(scriptData['views']))
	infoEmbed.add_field(name="Likes", value=str(scriptData['likeCount']))
	infoEmbed.add_field(name="Haters", value=str(scriptData['dislikeCount']))
	infoEmbed.add_field(name="ID", value=id)
	infoEmbed.add_field(name="Creator", value=f"{creator} {verified and ":white_check_mark:" or ""}")
	infoEmbed.add_field(name="Game", value=scriptData['game']['name'])
	infoEmbed.add_field(name="Created", value=created)
	infoEmbed.add_field(name="Verified Script", value=(scriptData['verified'] and "Yes" or "No"))


	if "keyLink" in scriptData and scriptData['keyLink'] != "":
		infoEmbed.add_field(name="Key", value=f"[Link]({scriptData['keyLink']})")
	else:
		infoEmbed.add_field(name="Key", value="Script is keyless")
	return infoEmbed

def createUserEmbed(data, profileLink):
	id = data['user']['_id']
	username = data['user']['username']
	verified = data['user']['verified'] and "Yes" or "No"
	role = data['user']['role']
	status = data['user']['status']
	followers = str(data['user']['followersCount'])
	following = str(data['user']['followingCount'])	
	joinDate = re.search(r"(\d\d\d\d-\d\d-\d\d)", data['user']['createdAt']).group(1)
	onlineDate = re.search(r"(\d\d\d\d-\d\d-\d\d)", data['user']['lastActive']).group(1)
	_discord = "No discord linked"
	pfp = f"https://scriptblox.com{data['user']['profilePicture']}"
	if "discord" in data['user'] and "id" in data['user']['discord']:
		_discord = f"<@{data['user']['discord']['id']}>"
	if status == "online":
		status = ":green_circle: Online"
	elif status == "idle":
		status = ":orange_circle: Idle"
	else:
		status = ":red_circle: Offline"
	if role != "user":
		if role == "owner":
			role = ":crown: Owner"
		else:
			role = ":star: Moderator"
	else:
		role = ":skull: User"
	infoEmbed = discord.Embed(title=username)
	infoEmbed.add_field(name="Role", value=role)
	infoEmbed.add_field(name="Status", value=status)
	infoEmbed.add_field(name="Followers", value=followers)
	infoEmbed.add_field(name="Following", value=following)
	infoEmbed.add_field(name="Verified", value=verified)
	infoEmbed.add_field(name="Join Date", value=joinDate)
	infoEmbed.add_field(name="Last Online", value=onlineDate)
	infoEmbed.add_field(name="User ID", value=id, inline=False)
	infoEmbed.add_field(name="Discord", value=_discord, inline=False)
	infoEmbed.add_field(name="Profile", value=f"[Click Me](https://scriptblox.com/u/{profileLink})")
	infoEmbed.set_thumbnail(url=pfp)
	return infoEmbed

# cmds
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if isinstance(message.channel, discord.DMChannel):
		await message.channel.send("no, use <#1420433036402491512>", file=discord.File("rule67.gif"))
		data = {"content": f"User {message.author} ({message.author.id}) DMed: {message.content}"}
		requests.post("If  you want to know when somebody DM's your bot, you can put a webhook here", json=data)
	else:
		await bot.process_commands(message)
        

@bot.command(brief="Validates how many bot accounts are working")
async def check(ctx):
	print("checking")
	success = 0
	tokens = get_tokens()
	await ctx.send(f"checking {len(tokens)} tokens")
	for token in tokens:
		res = session.get("https://scriptblox.com/api/notification/fetch", headers={"authorization": token})
		if res.status_code != 200:
			print(token, res.status_code)
			if res.json()['message'] == "User banned!":
				await ctx.send(f":x: BANNED ({res.json()['reason']})")
			else:
				await ctx.send(":x: " + res.json()['message'])
			continue
		res = res.json()
		try:
			if "notifications" in res:
				success += 1
		except:
			print(res, token)
			pass

	resultsEmbed = discord.Embed(title=f"Valid bots", description=f"{success}/{len(tokens)} work", color=0x77FF00)
	await ctx.send(embed=resultsEmbed)

@bot.command()
async def ping(ctx):
	await ctx.send(f":ping_pong: Pong! {bot.latency}ms")

@bot.command(brief="Gives [script] [amount] likes")
async def like(ctx, script, amount, _s=0):
	print("--- liking ---")
	_s = int(_s)
	if amount == "all":
		amount = len(get_tokens())
	else:
		try:
			amount = int(amount)
		except ValueError:
			await ctx.send("amount must be a number")
			return
	scriptLink = re.search("https://scriptblox.com/script/(.+)", script)
	if scriptLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/script/{scriptLink.group(1)}")
		if not data:
			await ctx.send("failed to get data, post may have been deleted or privated")
			return
		scriptData = data['script']
		id = scriptData['_id']
		title = scriptData['title']
		creator = scriptData['owner']['username']
		infoEmbed = makeInfoEmbed(id=id, creator=creator, scriptData=scriptData, title=title, color=0x6600FF, verified=scriptData['owner']['verified'])
		await ctx.send(content=f"liking {id} (this can take a while because of rate limits)", embed=infoEmbed)
		used = 0
		tokens = get_tokens()
		nowTime = time()
		for token in tokens:
			used += 1
			if used <= _s:
				continue
			if used > amount:
				break
			headers={
				"authorization": token
			}
			json = {
				"scriptId": id
			}
			s = session.post("https://scriptblox.com/api/script/like", headers=headers, json=json)
			print("like " + str(s.status_code) + " " + str(used))
			sleep(3)

		resultsEmbed = discord.Embed(title=f"Finished liking {id}", color=0x77FF00)
		await ctx.send(content=f"<@{ctx.author.id}> time: {time() - nowTime} seconds", embed=resultsEmbed)
	else:
		await ctx.send("invalid link")
		return

@bot.command(brief="Gives [script] [amount] dislikes")
async def dislike(ctx, script, amount, _s=0):
	print("--- disliking ---")
	_s = int(_s)
	if amount == "all":
		amount = len(get_tokens())
	else:
		try:
			amount = int(amount)
		except ValueError:
			await ctx.send("amount must be a number")
			return
	scriptLink = re.search("https://scriptblox.com/script/(.+)", script)
	if scriptLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/script/{scriptLink.group(1)}")
		if not data:
			await ctx.send("failed to get data, post may have been deleted or privated")
			return
		scriptData = data['script']
		id = scriptData['_id']
		title = scriptData['title']
		creator = scriptData['owner']['username']
		infoEmbed = makeInfoEmbed(id=id, creator=creator, scriptData=scriptData, title=title, color=0x6600FF, verified=scriptData['owner']['verified'])
		await ctx.send(content=f"disliking {id} (this can take a while because of rate limits)", embed=infoEmbed)
		used = 0
		tokens = get_tokens()
		nowTime = time()
		for token in tokens:
			used += 1
			if used <= _s:
				continue
			if used > amount:
				break
			headers={
				"authorization": token
			}
			json = {
				"scriptId": id
			}
			s = session.post("https://scriptblox.com/api/script/dislike", headers=headers, json=json)
			print("dislike " + str(s.status_code) + " " + str(used))
			sleep(3)

		resultsEmbed = discord.Embed(title=f"Finished disliking {id}", color=0x77FF00)
		await ctx.send(content=f"<@{ctx.author.id}> time: {time() - nowTime} seconds", embed=resultsEmbed)
	else:
		await ctx.send("invalid link")
		return
	
@bot.command(brief="Extracts the scriptId from link")
async def sid(ctx, link):
	scriptLink = re.search("https://scriptblox.com/script/(.+)", link)
	if scriptLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/script/{scriptLink.group(1)}")
		if not data:
			await ctx.send("failed to get data, post may have been deleted or privated")
			return
		scriptData = data['script']
		id = scriptData['_id']
		await ctx.send(id)
	else:
		await ctx.send("invalid link")
		return

@bot.command(brief="Gives you minor information about a script")
async def sinfo(ctx, link):
	scriptLink = re.search("https://scriptblox.com/script/(.+)", link)
	if scriptLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/script/{scriptLink.group(1)}")
		if not data:
			await ctx.send("failed to get data, post may have been deleted or privated")
			return
		scriptData = data['script']
		id = scriptData['_id']
		title = scriptData['title']
		creator = scriptData['owner']['username']
		infoEmbed = makeAdvancedInfoEmbed(id=id, creator=creator, scriptData=scriptData, title=title, color=0x6600FF, verified=scriptData['owner']['verified'])
		with open("upload/script.txt", "w", encoding="utf8") as f:
			f.write(scriptData['script'])
		await ctx.send(embed=infoEmbed)
		await ctx.send(file=discord.File("upload/script.txt"))
	else:
		await ctx.send("invalid link")
		return
	
@bot.command(brief="Extracts the userId from link")
async def uid(ctx, link):
	profileLink = re.search("https://scriptblox.com/u/(.+)", link)
	if profileLink:
		profileLink = profileLink.group(1)
	else:
		profileLink = link

	data = session.get(f"https://scriptblox.com/api/user/info/{profileLink}")
	if data.status_code != 200:
		await ctx.send(f"unknown fail (message: {data.json()['message']})")
		return
	data = data.json()

	id = data['user']['_id']
	await ctx.send(id)

@bot.command(brief="Gives you minor information about a user")
async def uinfo(ctx, link):
	if link == "voltex":
		return await ctx.send("that user is too retarded to search up")
	profileLink = re.search("https://scriptblox.com/u/(.+)", link)
	if profileLink:
		profileLink = profileLink.group(1)
	else:
		profileLink = link

	data = session.get(f"https://scriptblox.com/api/user/info/{profileLink}")
	if data.status_code != 200:
		await ctx.send(f"unknown fail (code: {data.status_code})")
		return
	data = data.json()

	infoEmbed = createUserEmbed(data, profileLink)

	await ctx.send(embed=infoEmbed)

@bot.command(brief="Removes [amount] of botted likes/dislikes from [script]")
async def remove(ctx, mode, link, amount):
	if amount == "all":
		amount = len(get_tokens())
	else:
		try:
			amount = int(amount)
		except ValueError:
			await ctx.send("amount must be a number")
			return
	scriptLink = re.search("https://scriptblox.com/script/(.+)", link)
	if scriptLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/script/{scriptLink.group(1)}")
		if not data:
			await ctx.send("fail to get post data maybe deleted or privated")
			return
	else:
		await ctx.send("invalid link")
		return
	
	tokens = get_tokens()
	used = 0
	if mode == "dislike" or mode == "like":
		await ctx.send(f"removing {data['script']['_id']} (could take long bc rate limits)")
		for token in tokens:
			used += 1
			if used > amount:
				break
			try:
				d = session.delete(f"https://scriptblox.com/api/script/{mode}/{data['script']['_id']}", headers={"authorization": token})
				print(d.status_code)
			except:
				print("hmm")
			sleep(3)
		await ctx.send("complete")

@bot.command(brief="Gives [username] [amount] followers [⚠ Exposes bots]")
async def follow(ctx, username, amount, _s=0):
	_s = int(_s)
	if amount == "all":
		amount = len(get_tokens())
	else:
		try:
			amount = int(amount)
		except ValueError:
			await ctx.send("amount must be a number")
			return
	profileLink = re.search("https://scriptblox.com/u/(.+)", username)
	if profileLink:
		profileLink = profileLink.group(1)
	else:
		profileLink = username
	if profileLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/user/info/{profileLink}")
		if not data:
			await ctx.send("profile doesnt exist")
			return

		successful = 0
		alreadyFollowed = 0
		used = 0
		tokens = get_tokens()
		nowTime = time()
		username = data['user']['username']
		id = data['user']['_id']
		await ctx.send(f"following {id} (this can take a while because of rate limits)")
		for token in tokens:
			used += 1
			if used <= _s:
				continue
			if used > amount:
				break
			headers={
				"authorization": token
			}
			json = {
				"userId": id
			}
			post = session.post("https://scriptblox.com/api/user/follow", headers=headers, json=json)
			message = post.json()['message']
			if post.status_code != 200 and (message != f"You're now following {username}" and message != "You're already following this user!" and message != "You cannot follow yourself!"):
				await ctx.send(f":x: failed to follow ({str(post.status_code)}, {message})")
				continue
			else:
				if message == "You're already following this user!":
					alreadyFollowed += 1
				successful += 1
			sleep(1.5)

		astr = alreadyFollowed > 0 and f" ({alreadyFollowed} already following)" or ""
		resultsEmbed = discord.Embed(title=f"Results for {username}", description=f"{successful}/{amount} success{astr}", color=0x77FF00)
		await ctx.send(content=f"time: {time() - nowTime} seconds", embed=resultsEmbed)
	else:
		await ctx.send("invalid link")
		return
	

@bot.command(brief="Unfollows a user")
async def unfollow(ctx, username, amount, _s=0):
	_s = int(_s)
	if amount == "all":
		amount = len(get_tokens())
	else:
		try:
			amount = int(amount)
		except ValueError:
			await ctx.send("amount must be a number")
			return
	profileLink = re.search("https://scriptblox.com/u/(.+)", username)
	if profileLink:
		profileLink = profileLink.group(1)
	else:
		profileLink = username
	if profileLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/user/info/{profileLink}")
		if not data:
			await ctx.send("profile doesnt exist")
			return

		successful = 0
		alreadyFollowed = 0
		used = 0
		tokens = get_tokens()
		nowTime = time()
		username = data['user']['username']
		id = data['user']['_id']
		await ctx.send(f"unfollowing {id} (this can take a while because of rate limits)")
		for token in tokens:
			used += 1
			if used <= _s:
				continue
			if used > amount:
				break
			headers={
				"authorization": token
			}
			json = {
				"userId": id
			}
			post = session.post("https://scriptblox.com/api/user/unfollow", headers=headers, json=json)
			message = post.json()['message']
			if post.status_code != 200 and (message != f"Unfollowed user {username}" and message != "Follow the user first!" and message != "You cannot follow yourself!"):
				await ctx.send(f":x: failed to unfollow ({str(post.status_code)}, {message})")
				continue
			else:
				if message == "Follow the user first!":
					alreadyFollowed += 1
				successful += 1
			sleep(1.5)

		astr = alreadyFollowed > 0 and f" ({alreadyFollowed} already following)" or ""
		resultsEmbed = discord.Embed(title=f"Results for {username}", description=f"{successful}/{amount} success{astr}", color=0x77FF00)
		await ctx.send(content=f"time: {time() - nowTime} seconds", embed=resultsEmbed)
	else:
		await ctx.send("invalid link")
		return

@bot.command(brief="Comments on a script [⚠ Exposes bots]")
async def comment(ctx, script, amount, _s=0):
	print("--- commenting ---")
	if len(ctx.message.attachments) == 0:
		await ctx.send("expected a json file of messages")
	file = await ctx.message.attachments[0].read()
	possible = jsonUtil.dumps(file.decode("utf-8"))
	_s = int(_s)
	if amount == "all":
		amount = len(get_tokens())
	else:
		try:
			amount = int(amount)
		except ValueError:
			await ctx.send("amount must be a number")
			return
	scriptLink = re.search("https://scriptblox.com/script/(.+)", script)
	if scriptLink:
		data = Posts.getScriptData(f"https://scriptblox.com/api/script/{scriptLink.group(1)}")
		if not data:
			await ctx.send("failed to get data, post may have been deleted or privated")
			return
		scriptData = data['script']
		id = scriptData['_id']
		title = scriptData['title']
		creator = scriptData['owner']['username']
		infoEmbed = makeInfoEmbed(id=id, creator=creator, scriptData=scriptData, title=title, color=0x6600FF, verified=scriptData['owner']['verified'])
		await ctx.send(content=f"commenting on {id} (this can take a while because of rate limits)", embed=infoEmbed)
		used = 0
		tokens = get_tokens()
		nowTime = time()
		for token in tokens:
			used += 1
			if used <= _s:
				continue
			if used > amount:
				break
			headers={
				"authorization": token
			}
			json = {
				"scriptId": id,
				"text": choice(possible)
			}
			s = session.post("https://scriptblox.com/api/comment/add", headers=headers, json=json)
			print("comment " + str(s.status_code) + " " + str(used))
			sleep(3)

		resultsEmbed = discord.Embed(title=f"Finished commenting on {id}", color=0x77FF00)
		await ctx.send(content=f"<@{ctx.author.id}> time: {time() - nowTime} seconds", embed=resultsEmbed)
	else:
		await ctx.send("invalid link")
		return

@bot.command(brief="Extracts content from a link using a GET request")
async def httpget(ctx, url):
	try:
		lsession = tls_client.Session()
		r = lsession.get(url, headers={
			"User-Agent": "Delta"
		})
		with open('upload/get.txt', 'wb') as f:
			f.write(r.content)
		await ctx.send(content=f"heres what i extracted", file=discord.File("upload/get.txt"))
	except Exception as e:
		await ctx.send("[INTERNAL_EXCEPTION]\n" + str(e))

@bot.command(brief="Tells you how many bots are saved. Does not validate")
async def bots(ctx):
	await ctx.send(f"{len(get_tokens())} saved. type !check to validate these")

@bot.command()
async def names(ctx):
	if ctx.author.id != 1215375161121833063:
		return await ctx.send("your are not permitted to use this, only apnff0x can use it")
	await ctx.send("extracting bot usernames (this might take a second)")
	lnames = ""
	idx = 0
	for token in get_tokens():
		idx += 1
		tokenInfo = session.get("https://scriptblox.com/api/user/me", headers={"authorization": token})
		if tokenInfo.status_code != 200: continue
		username = tokenInfo.json()['user']['username']
		lnames += f"[{idx}] {username}\n"
	with open("upload/names.txt", "w") as f:
		f.write(lnames + f"total: {len(get_tokens())}")
	await ctx.send(content="here are the usernames of the bots", file=discord.File("upload/names.txt"))

@bot.command(brief="Tells you which scriptblox admins are online")
async def mods(ctx):
	await ctx.send("checking mod activity")
	modders = ["Hypernova", "ThunderMods", "galitsacheatertg", "Omsin", "Depso", "wyvern", "SoniSins", "batusd3009", "Arcturus", "Rauwo"]
	for m in modders:
		r = session.get("https://scriptblox.com/api/user/info/" + m).json()
		if r['user']['status'] != "offline":
			e = createUserEmbed(r, m)
			await ctx.send(content=":warning: Moderator online", embed=e)
	await ctx.send("done")

# run
bot.run(token)
