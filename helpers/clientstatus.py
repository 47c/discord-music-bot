from utilities.definitions  import *

import discord
import time
import sys

class ClientStatus:
    def __init__(self, client: discord.Client):
        self.client: discord.Client             = client

        self.connected_to_channel               = False
        self.voice_client: discord.VoiceClient  = None

        self.last_update                        = 0

    def update_status(self):
        self.last_update = time.perf_counter()

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