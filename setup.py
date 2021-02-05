from setuptools import setup
setup(name='stripe-invoice-bot',
version='0.0.2',
description='Discord bot to create customers and generate invoices',
url='https://github.com/jmarhee/stripe-invoice-bot',
author='jmarhee',
author_email='jmarhee@interiorae.com',
license='MIT',
packages=['stripe_invoice_bot'],
python_requires='>=3.6',
entry_points = {
	'console_scripts': ['stripe-invoice-bot=stripe_invoice_bot.main:main']
},
install_requires=[
	"discord",
	"stripe",
	"tabulate"
],
zip_safe=False)
