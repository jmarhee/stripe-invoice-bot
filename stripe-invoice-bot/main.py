import os
import discord
from dotenv import load_dotenv
from stripe_tools import list_customers, create_customer, list_invoices, create_invoice, customer_name
from discord_functions import task_router

#load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
approved = os.environ['DISCORD_APPROVED_BOT'].split(",")

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_ready():
	guild_count = 0
	for guild in client.guilds:
		print(f"-- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("StripeCourier is in " + str(guild_count) + " servers.")

@client.event
async def on_message(message):
	message_content = message.content
	if message_content == "help":
		reply = "Commands:\nnew invoice [email] [amount]\nnew customer [name] [email]\nlist invoices\nlist customers"
		await message.channel.send(reply)
	elif str(message.author) in approved:
		reply = task_router(message_content)
		print(reply)
		await message.channel.send(reply)
	else:
		reply = "You are not authorized to use this app in this server."
		message.channel.send(reply)
		print(str(message.author) + ": " + reply)

client.run(TOKEN)


