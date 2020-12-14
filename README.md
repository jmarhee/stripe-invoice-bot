# Stripe Invoice Bot

A Python-powered Discord bot to create customers and invoices with Stripe.

![arthur from 2001 series "the tick"](https://www.syfy.com/sites/blastr/files/images/assets_c/2011/12/the-tick-david-burke-thumb-330x440-79351.jpg)

## Setup

This requires, both, a Stripe API token and a [Discord Bot Token](https://medium.com/better-programming/coding-a-discord-bot-with-python-64da9d6cade7).

These will need to be set to their respective values:

`STRIPE_API_TOKEN`
`DISCORD_TOKEN`

and then the approved users in your server who can use this bot:

`DISCORD_APPROVED_BOT="user1#id,user2#id"`

These are handled as environmental variables in the application, not from a configuration, so if you plan to use the Docker image, the command will be as follows:

```bash
docker build -t stripe-invoice-bot . ; \
docker run -d --name stripe-invoice-bot -e STRIPE_API_TOKEN=$STRIPE_API_TOKEN \
-e DISCORD_TOKEN=$DISCORD_TOKEN \
-e DISCORD_APPROVED_BOT=$DISCORD_APPROVED_BOT \
stripe-invoice-bot
```

## Running the Bot

You can, either, build the Dockerfile (using `docker build -t stripe-invoice-bot .`) or install the package using `pip`:

```
python3 -m pip install git+https://git-central.openfunction.co/jmarhee/stripe-invoice-bot.git@main
```

then running `stripe-invoice-bot` to start the bot process. It is recommended that this be managed by something like `supervisord` or another process manager.

If you are a supervisord user, a configuration like this should suffice:

```
[program:stripe-invoice-bot]
command=${YOUR_PYTHON_PKGS_PATH}/bin/stripe-invoice-bot 
autostart=true
autorestart=true
stderr_logfile=/var/log/stripe-invoice-bot.err.log
stdout_logfile=/var/log/stripe-invoice-bot.out.log
environment=DISCORD_TOKEN="",DISCORD_APPROVED_BOT="",STRIPE_API_KEY=""
```

then reread and update supervisor.

## Discord Commands

You can list `invoices`, `items`, or `customers` using:

```
list ${resource}
```

and delete any resource using:

```
delete ${resource} ${resource_id}
```

which you can find the ID for using the above `list` command format.

To create a customer record, open your Direct Message to Stripe Invoicer Bot, and send:

```
new customer customer@domain.com phonenumber FirstName LastName OtherData
```

You will receive a response like:

```
Customer name (name@email.com) created with id cus_ID
```

where `cus_ID` will be their customer ID, which you'll need to generate invoices.

You can add items to to be invoiced by running:

```
new item customer_ID amount description
```

and add as many as you'd like before proceeding to generate a draft invoice.

To generate a draft invoice, you can send the bot:

```
new invoice cus_ID
```

when the invoice is ready to be sent, you can use the returned Invoice ID (`in_XXXXX`) to tell the bot to send to the email on file:

```
send invoice in_XXXX
```
