#!/bin/env python3

import discord
import asyncio
import os
import re
from datetime import datetime
from urllib.parse import urlparse

regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"


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
        if link.hostname == "twitter.com":
            return link._replace(netloc='vxtwitter.com').geturl()
        else:
            return False

# Instanciate a client object and start it. 
client = MyClient(con) 
asyncio.create_task(client.start(os.environ['DISCORD_TOKEN']))