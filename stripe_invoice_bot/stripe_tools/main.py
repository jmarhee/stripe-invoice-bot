import requests
import stripe
import os
from datetime import date

stripe.api_key = os.environ['STRIPE_API_KEY']

def customer_name(customer):
	customer_ret = stripe.Customer.retrieve(customer)
	customer = {
		"id": customer_ret.id
	}
	if hasattr(customer_ret, 'name'):
		customer['name'] = customer_ret.name
	else:
		customer['name'] = "N/A"
	if hasattr(customer_ret, 'email'):
		customer['email'] = customer_ret.email
	else:
		customer['email'] = "N/A"
	return customer

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

def create_customer(name,email,phone):
	customer = stripe.Customer.create(name=name,email=email,phone=phone)
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
			"total": "$" + str((invoice.total / 100)), 
			"status": invoice.status 
		}
		invoice_status.append(i)
	return invoice_status	

def list_items():
	items = stripe.InvoiceItem.list()
	item_status = []
	for item in items['data']:
		item_status = []
		i = {
			"id": item.id,
			"customer": item.customer,
			"description": item.description,
			"amount": "$" + str((item.amount / 100))
		}
		item_status.append(i)
	return item_status

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

def create_invoice_item(customer, amount_due, description):
	item = stripe.InvoiceItem.create(
		customer=customer,
		price=create_price(amount_due, customer),
		description=description
	)
	return item

def fast_create_invoice(customer, amount_due, description):
	#Creates an invoice for a newly created item at bill-time.
	create_invoice_item(customer, amount_due)
	invoice = stripe.Invoice.create(
			customer=customer,
			description=description,
			collection_method="send_invoice",
			days_until_due=7
		)
	invoice_data = { "id": invoice.id, "customer_email": invoice.customer_email, "status": "DRAFT" }
	return invoice_data

def create_invoice(customer, description):
	#Creates an invoice from all outstanding items (ideal for periodic invoicing of all charges that period).
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

def delete_customer(customer):
	delete = stripe.Customer.delete(customer)
	return delete

def delete_invoice(invoice):
	delete = stripe.Invoice.delete(invoice)
	return delete

def delete_item(item):
	delete = stripe.InvoiceItem.delete(item)
	return delete
