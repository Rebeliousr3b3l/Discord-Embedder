import os
import discord
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if "twitter" in message.content and not "vxtwitter" in message.content:
            print("I see twitter in that message!")
            link = urlparse(message.content)
            result = link._replace(netloc='vxtwitter.com').geturl()
            print(result)
            await message.reply(content = result)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)