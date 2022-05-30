import os
from glob import glob
import sys
import traceback

from disnake.ext.commands import *
from disnake import Intents

prefix = "&"
OWNER_IDS = []
COGS = [path.split("\\")[1][:-3] for path in glob("./lib/cogs/*py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"        {cog} ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Iteria(Bot):
    def __init__(self):
        self.prefix = prefix
        self.ready = False
        self.token = os.environ["bot_token2"]
        self.cogs_ready = Ready()
        self.version: str = ""
        self.intent = Intents.default()
        self.intent.messages = True
        super().__init__(command_prefix=self.prefix, owner_ids=OWNER_IDS, intents=self.intent)

    def run(self, version):
        self.version = version
        print("Running setup...")
        self.setup()

        print("running bot...")
        super().run(self.token, reconnect=True)

    def setup(self):
        for cog in COGS:
            try:
                print(f"    loadin {cog}")
                self.load_extension(f"lib.cogs.{cog}")
            except NoEntryPointError as e:
                print(f"Ignoring exception in loading cog: {cog}\nNo setup found", file=sys.stderr)
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            except ExtensionFailed as e:
                print(f"Ignoring exception in loading cog: {cog}\nThe extension or its setup had an execution error"
                      , file=sys.stderr)
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            else:
                print(f"    {cog} loaded")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")