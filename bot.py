#!/bin/env python3

import discord
import asyncio
import os
import re
from datetime import datetime
from urllib.parse import urlparse

# https://stackoverflow.com/a/840110
regex=r"(?P<url>https?://[^\s]+)"


class MyClient(discord.Client):
    def __init__(self, con):
        """Called upon instanciation"""
        self.con = con
        super().__init__()
        
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    
    async def on_message(self, message):
        if self.user.id == message.author.id:
            return
        
        if "||" or ("<" and ">") in message.content:
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
            await asyncio.sleep(2)
            await message.edit(suppress=True)
    
    # if url contains a twitter link, replace the hostname
    # with vxtwitter. Returns False if not a twitter link.
    def handle_url(self, url):
        link = urlparse(url)
        if link.hostname == "twitter.com" and link.query == "s=20":
            return link._replace(netloc='vxtwitter.com').geturl()
        else:
            return False

# Instanciate a client object and start it. 
client = MyClient(con) 
asyncio.create_task(client.start(os.environ['DISCORD_TOKEN']))