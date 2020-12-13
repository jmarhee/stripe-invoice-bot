import os
import discord
from dotenv import load_dotenv
from .stripe_tools import *

TOKEN = os.environ['DISCORD_TOKEN']
approved = os.environ['DISCORD_APPROVED_BOT'].split(",")

client = discord.Client()

def task_router(message):
        message_opts = message.split(" ")
        help = {"Usage": "Commands:\nnew invoice [email] [amount]\nnew customer [email] [name]\nlist invoices\nlist customers"}
        if message_opts[0] == "new":
                if message_opts[1] == "invoice":
                        customer = message_opts[2]
                        amount = message_opts[3]
                        name = customer_name(customer)
                        description = "Tutoring session for %s" % (name)
                        task = create_invoice(customer,amount,description)
                elif message_opts[1] == "customer":
                        name = " ".join(message_opts[3:len(message_opts)])
                        email = message_opts[2]
                        task = create_customer(name,email)
        elif message_opts[0] == "send":
                if message_opts[1] == "invoice":
                        invoice = message_opts[2]
                        task = send_invoice(invoice)
        elif message_opts[0] == "list":
                if message_opts[1] == "customers":
                        task = list_customers()
                elif message_opts[1] == "invoices":
                        task = list_invoices()
        return task
#load_dotenv()
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

def main():
	client.run(TOKEN)
