#!/bin/env python3

import discord
import asyncio
import os
import re
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# https://stackoverflow.com/a/840110
regex=r"(?P<url>https?://[^\s]+)"

#Set to True if one of the links is a Facebook link.
facebook = False

class MyClient(discord.Client):
    #def __init__(self, con):
    #    """Called upon instanciation"""
    #    self.con = con
    #    super().__init__()
        
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    
    async def on_message(self, message):
        global facebook
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
            if len(replacements) == 5:
                break
            url = self.handle_url(match)
            if url:
                replacements.append(url)
        
        # only send messages if there were matches
        if len(replacements) > 0:
            # join the urls together by newlines
            if facebook:
                await message.reply(content = "Mitigated FB's tracking. *Squeak!*\n" + "\n".join(replacements), mention_author=False, suppress_embeds=True)
                await message.delete()
                facebook = False
            else:
                await message.reply(content = "\n".join(replacements), mention_author=False)
                await message.add_reaction('🦦')
                await asyncio.sleep(4)
                await message.edit(suppress=True)
    
    # if url contains a twitter link, replace the hostname
    # with vxtwitter. Returns False if not a twitter link.
    def handle_url(self, url):
        link = urlparse(url)

        match link.hostname:
            case "www.x.com":
                return link._replace(netloc='fxtwitter.com').geturl()
            
            case "www.tiktok.com":
                if ("@" in link.path):
                    return link._replace(netloc='vxtiktok.com').geturl()
                else:
                    expanded = requests.get(url, allow_redirects=False)
                    link = urlparse(expanded.headers['location'])
                    return link._replace(netloc='vxtiktok.com').geturl()
                
            case "www.instagram.com":
                if (re.search("reels", link.path) != None):
                    return link._replace(netloc='kkinstagram.com').geturl()
                else:
                    return False
            
            case "www.reddit.com":
                return link._replace(netloc="rxddit.com").geturl()
            
            case "www.facebook.com":
                if (re.search("share", link.path) != None):
                    expanded = requests.get(url, allow_redirects=False)
                    link = urlparse(expanded.headers['location'])
                    global facebook
                    facebook = True
                    return link._replace(query="").geturl()
                else:
                    return False
            
            case _:
                print("Hit")
                return False


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)