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

## Discord Commands

To create a customer record, open your Direct Message to Stripe Invoicer Bot, and send:

```
new customer FirstLast customer@domain.com
```

You will receive a response like:

```
Customer name (name@email.com) created with id cus_ID
```

where `cus_ID` will be their customer ID, which you'll need to generate invoices.

To generate a draft invoice, you can send the bot:

```
new invoice cus_ID amount
```

when the invoice is ready to be sent, you can use the returned Invoice ID (`in_XXXXX`) to tell the bot to send to the email on file:

```
send invoice in_XXXX
```


