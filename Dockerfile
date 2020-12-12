FROM python:3.8

ENV DISCORD_TOKEN ""
ENV DISCORD_APPROVED_BOT ""
ENV STRIPE_API_KEY ""

RUN mkdir /app

ADD requirements.txt /app/requirements.txt
ADD discord_functions.py /app/discord_functions.py
ADD stripe_tools.py /app/stripe_tools.py
ADD main.py /app/main.py

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRPOINT python3 main.py
CMD []
