import os
from glob import glob
import sys
import traceback

from disnake.ext.commands import *
from disnake import Intents

#Set the bot's prefix, creating an empty list for owner ids and initialize a list for cogs stored in ./lib/cogs/
prefix = "&"
OWNER_IDS = []
COGS = [path.split("\\")[1][:-3] for path in glob("./lib/cogs/*py")]


class Ready(object): #This class comunicates the status of the cogs
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False) #Set all cogs to False

    def ready_up(self, cog):
        setattr(self, cog, True) #Set the cog to True
        print(f"        {cog} ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS]) #Return True if all cogs are ready

class MyBot(Bot):#This is the main bot class
    def __init__(self):
        self.prefix = prefix
        self.ready = False
        self.token = os.environ["bot_token2"] #It is suggested to hide the token, in this case an environment variable is used
        self.cogs_ready = Ready() #Initialize the Ready class
        self.version: str = ""
        self.intent = Intents.default() #Setting the default intents
        self.intent.message_content = True #Enabling the message_content intent
        super().__init__(command_prefix=self.prefix, owner_ids=OWNER_IDS, intents=self.intent) #Calling the super constructor

    def run(self, version): #This method runs the bot
        self.version = version
        print("Running setup...")
        self.setup() #Run the setup

        print("running bot...")
        super().run(self.token, reconnect=True) #Once the setup is ready, we can connect the bot to discord API

    def setup(self): #This method loads all cogs
        for cog in COGS:
            try:
                print(f"    loadin {cog}")
                self.load_extension(f"lib.cogs.{cog}") #Load the cog
                #Since the cogs are stored and loaded automatically from a folder, it is not necessary to handle
                #ExtensionNotFound and ExtensionAlreadyLoaded errors
            except NoEntryPointError as e: #Handle the NoEntryPointError and print the exception in the console
                print(f"Ignoring exception in loading cog: {cog}\nNo setup found", file=sys.stderr)
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            except ExtensionFailed as e: #Handle the ExtensionFailed and print the exception in the console
                print(f"Ignoring exception in loading cog: {cog}\nThe extension or its setup had an execution error"
                      , file=sys.stderr)
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            else:
                print(f"    {cog} loaded")

    async def on_connect(self): #When the bot connects to discord, it will print the following message
        print("bot connected")

    async def on_disconnect(self):#When the bot disconnects from discord, it will print the following message
        print("bot disconnected")
