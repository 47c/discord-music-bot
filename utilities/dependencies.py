import discord
from discord import app_commands

import yt_dlp as youtube_client
import asyncio
import time

from utilities.definitions import *
from utilities.logs import *

class ClientStatus:
    def __init__(self, client: discord.Client):
        self.client = client

        self.connected_to_channel = [False, None]
        self.unused_for = 0

        self.last_update = 0

        self.kill = False

    def update_status(self, interaction: discord.Interaction, voice_client: discord.VoiceClient = None):
        self.last_update = time.perf_counter()
        
        self.connected_to_channel[0] = interaction.guild.voice_client in client.voice_clients
        if voice_client:
            self.connected_to_channel[1] = voice_client
        elif not self.connected_to_channel[0]:
            self.connected_to_channel[1] = None

    async def timeout_handler(self):
        while not self.kill:
            if time.perf_counter() - self.last_update >= VOICE_TIMEOUT:
                if self.connected_to_channel[0] and not self.connected_to_channel[1] is None:
                    await self.connected_to_channel[1].disconnect()

            time.sleep(0.1)

class GuildData:
    def __init__(self, client: discord.Client):
        self.client = client

intents: discord.Intents        = discord.Intents.default()
intents.message_content         = intents.members = True

client: discord.Client          = discord.Client(intents=intents)
tree: app_commands.CommandTree  = app_commands.CommandTree(client)

client_status: ClientStatus     = ClientStatus(client)

timeout_thread                  = threading.Thread(name='voice timeout', target=asyncio.run, args=(client_status.timeout_handler(),))