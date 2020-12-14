FROM python:3.8

ENV DISCORD_TOKEN ""
ENV DISCORD_APPROVED_BOT ""
ENV STRIPE_API_KEY ""

RUN pip install stripe-invoice-bot

ENTRYPOINT stripe-invoice-bot
CMD []
