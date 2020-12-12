
from stripe_tools import customer_name, list_customers, create_customer, list_invoices, create_invoice, send_invoice

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
		
