import discord

from discord                import app_commands
from unsync.unsync          import unsync

from utilities.definitions  import *

from helpers.clientstatus   import *
from helpers.youtube        import *
from helpers.queue          import *

import time

class GuildData:
    def __init__(self, client: discord.Client):
        self.client: discord.Client     = client
        self.status: ClientStatus       = ClientStatus(client)
        self.audio_queue: AudioQueue    = AudioQueue()

@unsync
async def timeout_handler():
    global GLOBAL_KILLTHREADS, guild_data

    # run timeout handler for each guild once every 500ms
    while not GLOBAL_KILLTHREADS:
            data: GuildData
            for data in guild_data.values():
                await data.status._timeout_handler()

            time.sleep(0.5)

intents: discord.Intents            = discord.Intents.default()
intents.message_content             = intents.members = True

client: discord.Client              = discord.Client(intents=intents)
tree: app_commands.CommandTree      = app_commands.CommandTree(client)