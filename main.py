import discord
import os
from dotenv import load_dotenv
from load import *

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('úgymond'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!szerda'):
        torol()
        heti_scrape()
        keres()
        formaz()
        leiras = open('./leiras.txt', "r", encoding="utf8")
        file = discord.File('./aktualis_kutya.jpg')
        embed_dog = discord.Embed(title="Heti menő kutyanév:", color=0x71368a)
        embed_dog.set_author(name="Heti kutya", icon_url='https://cdn.discordapp.com/avatars/942463306717888564/125140ff559868c9de4385418771d4d1.png')
        embed_dog.set_image(url='attachment://aktualis_kutya.jpg')
        embed_dog.set_footer(text=leiras.read())
        await message.channel.send(file=file, embed=embed_dog)

client.run(TOKEN)
