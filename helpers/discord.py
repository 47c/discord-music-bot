import discord

from discord                import app_commands
from unsync.unsync          import unsync

from utilities.definitions  import *
from helpers.youtube        import *
from helpers.queue          import *

import time
import sys

class ClientStatus:
    def __init__(self, client: discord.Client):
        self.client: discord.Client             = client

        self.connected_to_channel               = False
        self.voice_client: discord.VoiceClient  = None

        self.last_update                        = 0

    def update_status(self, interaction: discord.Interaction, voice_client: discord.VoiceClient = None):
        self.last_update = time.perf_counter()
        
        self.connected_to_channel = interaction.guild.voice_client in client.voice_clients
        if voice_client:
            self.voice_client = voice_client
        elif not self.connected_to_channel:
            self.voice_client: discord.VoiceClient = None

    async def _timeout_handler(self):
        # check if time since last update has passed timeout threshold
        if time.perf_counter() - self.last_update < VOICE_TIMEOUT:
            return
        
        # make sure we're connected to a voice channel
        if not self.connected_to_channel or self.voice_client is None:
            return

        # disconnect from channel
        await self.voice_client.voice_disconnect()

        # set last_update to maxint
        self.last_update = sys.maxsize

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