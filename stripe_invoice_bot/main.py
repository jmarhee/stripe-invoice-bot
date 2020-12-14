import os
import discord
from .stripe_tools import *
from .data_table import *
from datetime import datetime

TOKEN = os.environ['DISCORD_TOKEN']
approved = os.environ['DISCORD_APPROVED_BOT'].split(",")

client = discord.Client()

def task_router(message):
	message_opts = message.split(" ")
	if message_opts[0] == "new":
		if message_opts[1] == "fast_invoice":
			customer = message_opts[2]
			amount = message_opts[3]
			name = customer_name(customer)
			description = "%s invoice for %s:" % (str(datetime.now().strftime("%m/%d/%Y")),name) + " " + " ".join(message_opts[4:len(message_opts)])
			task = fast_create_invoice(customer,amount,description)
		elif message_opts[1] == "item":
			customer = message_opts[2]
			amount = message_opts[3]
			name = customer_name(customer)
			description = "%s:" % (str(datetime.now().strftime("%m/%d/%Y"))) + " " + " ".join(message_opts[4:len(message_opts)])
			task = create_invoice_item(customer,amount,description)
		elif message_opts[1] == "invoice":
			customer = message_opts[2]
			name = customer_name(customer)
			description = "%s invoice for %s:" % (str(datetime.now().strftime("%m/%d/%Y")),name) + " " + " ".join(message_opts[4:len(message_opts)])
			task = create_invoice(customer,description)
		elif message_opts[1] == "customer":
			name = " ".join(message_opts[4:len(message_opts)])
			email = message_opts[2]
			phone = message_opts[3]
			task = create_customer(name,email,phone)
	elif message_opts[0] == "send":
		if message_opts[1] == "invoice":
			invoice = message_opts[2]
			task = send_invoice(invoice)
	elif message_opts[0] == "list":
		if message_opts[1] == "customers":
			task_data = list_customers()
			task = generate_table(task_data)
		elif message_opts[1] == "invoices":
			task_data = list_invoices()
			task = generate_table(task_data)
		elif message_opts[1] == "items":
			task_data = list_items()
			task = generate_table(task_data)
	elif message_opts[0] == "delete":
		if message_opts[1] == "customer":
			task = delete_customer(message_opts[2])
		elif message_opts[1] == "invoice":
			task = delete_invoice(message_opts[2])
		elif message_opts[1] == "item":
			task = delete_item(message_opts[2])
	return task

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
	message_data = {
		"author": str(message.author),
		"content": message.content,
		"authorized": str(message.author) in approved
	}
	today = date.today()
	if message_data['content'] == "help":
		reply = "Commands:\nnew invoice [customer]\nnew item [customer] [amount] [description]\nnew customer [email] [phone] [name, or other ID]\nlist [invoices,customers,items]"
		await message.channel.send(reply)
	elif message_data['authorized'] == True:
		reply = task_router(message_data['content'])
		print(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) 
		print(message_data)
		await message.channel.send(reply)
	else:
		reply = "You are not authorized to use this app in this server."
		# message.channel.send(reply)
		print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		print(message_data)

def main():
	client.run(TOKEN)
