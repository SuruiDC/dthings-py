from bs4 import BeautifulSoup
import pandas as pd
import requests

def getInfoBot(id=str):
	page=requests.get(f"https://discordthings.com/bot/{id}")
	res=BeautifulSoup(page.content, "html.parser")

	if res.title.text.strip() == "DiscordThings | 404":
		raise TypeError("The bot is not registered on the page")

	count=0
	biografy=[]
	recuards=[]
	tags=[]
	page=[]
	for i in res.find_all("meta"):
		if count == 4:
			pass
		else:
			biografy.append(i.get("content"))
			count=count+1

	for x in res.find_all("p", class_="box-2"):
		recuards.append(x.text.strip())

	for u in res.find_all("span", class_="tag botTags mb-1"):
		tags.append(u.text)

	for y in res.find_all("a", class_="mt-3"):
		if "discord.gg" not in y.get("href"):
			page.append(y.get("href"))
		else:
			pass
	info={
		"Name": biografy[0],
		"ID": id,
		"Avatar": biografy[2],
		"Description": biografy[3],
		"Prefix": recuards[0].replace("Prefix: ", ""),
		"Servidores": recuards[1].replace("Servidores: ", ""),
		"Votos": recuards[2].replace("Votos: ", ""),
		"Invitaciones": recuards[3].replace("Invitaciones: ", ""),
		"Tags": tags,
		"Page": page,
		"Owner": res.find_all("h3", class_="has-text-white is-size-6")[1].text
	}

	return info

def getUser(id=str):
	page=requests.get(f"https://discordthings.com/u/{id}")
	res=BeautifulSoup(page.content, "html.parser")

	if res.title.text.strip() == "DiscordThings | 404":
		raise TypeError("The user is not registered on the page")

	lots=res.find_all("span", class_="heading has-text-white")
	badges=[]
	points=""
	staff=bool
	bots=[]
	avatars=[]
	descriptions=[]
	votes=[]
	invites=[]
	names=[]
	for i in res.find_all("span", class_="bg-dark tag is-dark mt-1 w-100"):
		if "Votos: " not in i.text:
			invites.append(i.text.replace("Invites: ", ""))
		else:
			votes.append(i.text.replace("Votos: ", ""))

	for i in res.find_all("img", class_="img-fluid"):
		avatars.append(i.get("src"))

	for i in res.find_all("span", class_="tooltiptext"):
		badges.append(i.text)

	for i in res.find_all("p", class_="card-text has-text-white"):
		descriptions.append(i.text)

	for i in res.find_all("strong", class_="card-title has-text-white is-3"):
		names.append(i.text)
	if "Puntos: " not in badges[0]:
		points="0"
		staff=False
	else:	
		points=badges[0].replace("Puntos: ", "")
		badges.pop(0)
		staff=True

	for i in range(len(avatars)):
		bots.append({
			"Name": names[i],
			"Avatar": avatars[i],
			"Description": descriptions[i],
			"Votes": votes[i],
			"Invites": invites[i]
		})

	info={
		"Username": res.find_all("p", class_="UserName is-size-5 has-text-white")[0].text.strip(),
		"ID": id,
		"Avatar": res.find_all("img", class_="rounded-circle")[0].get("src"),
		"Description": res.find_all("p", class_="has-text-white")[1].text.strip(),
		"Votos": lots[0].text.replace("\n", ""),
		"LastSession": lots[1].text.strip(),
		"Staff": staff,
		"Points": points,
		"Badges": badges,
		"Bots": bots
	}
	return info
	