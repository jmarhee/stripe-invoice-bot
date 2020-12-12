import os
import discord
from dotenv import load_dotenv

def task_router(message):
        message_opts = message.split(" ")
        help = {"Usage": "Commands:\nnew invoice [email] [amount]\nnew customer [name] [email]\nlist invoices\nlist customers"}
        if message_opts[0] == "new":
                if message_opts[1] == "invoice":
                        customer = message_opts[2]
                        amount = message_opts[3]
                        name = customer_name(customer)
                        description = "Tutoring session for %s" % (name)
                        task = create_invoice(customer,amount,description)
                elif message_opts[1] == "customer":
                        name = message_opts[2]
                        email = message_opts[3]
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

def main():
	client.run(TOKEN)


import requests
import stripe
import os
from datetime import date

stripe.api_key = os.environ['STRIPE_API_KEY']

def customer_name(customer):
        customer_ret = stripe.Customer.retrieve(customer)
        return { "id": customer, "name": customer_ret.name, "email": customer_ret.email }

def list_customers():
	customer_data = []
	for customer in stripe.Customer.list()['data']:
		cust = {}
		cust['id'] = customer.id
		cust['name'] = customer.name
		cust['email'] = customer.email
		cust['phone'] = customer.phone
		customer_data.append(cust)
	return customer_data

def create_customer(name,email):
	customer = stripe.Customer.create(name=name,email=email)
	return "Customer %s (%s) created with id %s" % (customer.name, customer.email, customer.id)

def list_invoices():
	invoices = stripe.Invoice.list()
	invoice_status = []
	for invoice in invoices['data']:
		i = { 
			"id": invoice.id, 
			"customer": invoice.customer, 
			"email": invoice.customer_email, 
			"name": invoice.customer_name, 
			"total": invoice.total, 
			"status": invoice.status 
		}
		invoice_status.append(i)
	return invoice_status	

def date_billed():
	today = date.today()
	current = today.strftime("%B %d, %Y")
	return str(current)

def create_price(amount_due, customer):
	price = stripe.Price.create(
			unit_amount=int(int(amount_due) * 100),
			currency="usd",
			product_data={"name": "%s (%s)" % (customer,date_billed())},
			metadata={"customer":customer, "date": date_billed()}
		)
	return price.id

def create_invoice_item(customer, amount_due):
	item = stripe.InvoiceItem.create(
		customer=customer,
		price=create_price(amount_due, customer),
	)
	return item

def create_invoice(customer, amount_due, description):
	create_invoice_item(customer, amount_due)
	invoice = stripe.Invoice.create(
			customer=customer,
			description=description,
			collection_method="send_invoice",
			days_until_due=7
		)
	invoice_data = { "id": invoice.id, "customer_email": invoice.customer_email, "status": "DRAFT" }
	return invoice_data

def send_invoice(invoice):
	invoice_sent = stripe.Invoice.send_invoice(invoice)
	sending = { "invoice": invoice, "email": invoice_sent.customer_email }
	return sending
