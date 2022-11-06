from discord import *
import os

client = Client(intents=Intents.default())

@client.event
def on_message(message):
   pass


client.run(os.getenv("TOKEN"))

