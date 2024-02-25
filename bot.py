#!/bin/env python3

import discord
import asyncio
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# https://stackoverflow.com/a/840110
regex=r"(?P<url>https?://[^\s]+)"


class MyClient(discord.Client):
    #def __init__(self, con):
    #    """Called upon instanciation"""
    #    self.con = con
    #    super().__init__()
        
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    
    async def on_message(self, message):
        #don't send message if it's from the bot
        if self.user.id == message.author.id:
            return
        
        #Checking if the link is unembedded
        if (re.search(r"<.*>", message.content) != None):
            return
        
        #Checking if the link is hidden.
        if (re.search(r"\|\|.*\|\|", message.content) != None):
            return

        # find all urls in the message content, store them in
        # an array if they are twitter links
        matches = re.findall(regex, message.content)
        replacements = []
        for match in matches:
            url = self.handle_url(match)
            if url:
                replacements.append(url)
        
        # only send messages if there were matches
        if len(replacements) > 0:
            # join the urls together by newlines
            await message.reply(content = "\n".join(replacements))
            await asyncio.sleep(4)
            await message.edit(suppress=True)
    
    # if url contains a twitter link, replace the hostname
    # with vxtwitter. Returns False if not a twitter link.
    def handle_url(self, url):
        link = urlparse(url)
        if (link.hostname == "twitter.com" or link.hostname == "x.com") and link.query == "s=20":
            return link._replace(netloc='vxtwitter.com').geturl()
        
        elif (link.hostname == "tiktok.com" or link.hostname == "www.tiktok.com"):
            return link._replace(netloc='vxtiktok.com').geturl()
        
        elif (link.hostname == "instagram.com" or link.hostname == "www.instagram.com"):
            return link._replace(netloc='ddinstagram.com').geturl()
        
        else:
            return False


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)



