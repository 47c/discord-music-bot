from helpers.clientstatus   import *
from helpers.entry          import *
from helpers.stream         import *
from helpers.youtube        import *

from utilities.logs         import *
from utilities.definitions  import *

from typing                 import Dict, List
from unsync                 import unsync

from copy import copy
import datetime
import discord
import re

class AudioQueue:
    def __init__(self):
        self.filters = {
            'pitch': 1.0,
            'tempo': 1.0,
            'bass': 0
        }

        self.queue: List[AudioEntry]            = list()
        self.client_status: ClientStatus        = None

        self.buffering                          = False
        self.transition                         = False

        self.update_filters()

    def update_filters(self, pitch: float = None, tempo: float = None, bass: int = None):
        if pitch:
            self.filters['pitch'] = pitch
        if tempo:
            self.filters['tempo'] = tempo
        if bass:
            self.filters['bass'] = bass

        if pitch or tempo or bass:
            Thread(target=self.apply_changes).start()

    def apply_changes(self):
        if not self.client_status or not self.client_status.voice_client or not self.client_status.voice_client.is_playing():
            return
        
        if len(self.queue) < 1:
            return

        self.transition = True

        self.client_status.voice_client.stop()
        self.queue[0].seek = str(
            datetime.timedelta(seconds=
                               time.time() - self.queue[0].epoch
            )
        )

        self._play_transition()

        self.transition = False

    def _options(self):
        pitch   = self.filters['pitch']
        tempo   = self.filters['tempo']
        bass    = self.filters['bass']

        return f'-vn -filter:a "rubberband=pitch={pitch}, rubberband=tempo={tempo}, bass=gain={bass}"'

    async def output_queue(self):
        output = 'empty queue'
        if len(self.queue) < 1:
            return output
        
        output = '```'
        entry: AudioEntry
        for index, entry in enumerate(self.queue):
            output += f'{index + 1} -> {entry.title}\n'
        
        output += '```'

        return output
    
    async def output_filters(self):
        output = '```'
        for filter, value in self.filters.items():
            output += f'{filter} -> {value}\n'
        output += '```'

        return output

    def push(self, entry):
        if type(entry) == YoutubeVideoData:
            entry: YoutubeVideoData
            self.queue.append(AudioEntry(title=entry.title,
                                         thumbnail=entry.thumbnail,
                                         url=entry.url,
                                         buffer=entry.buffer))
            
            return
        
        self.queue.append(entry)

    def pop(self, index = None):
        self.queue.pop(index) if index else self.queue.pop()

    def pause(self):
        if self.client_status and self.client_status.voice_client and self.client_status.voice_client.is_playing():
            self.client_status.voice_client.pause()
            return 'song paused'
        
        return 'currently not playing'

    def resume(self):
        if self.client_status and self.client_status.voice_client and self.client_status.voice_client.is_paused():
            self.client_status.voice_client.resume()
            return 'song paused'
        
        return 'currently not paused'

    def stop(self):
        if self.client_status and self.client_status.voice_client and self.client_status.voice_client.is_playing():

            self.client_status.voice_client.stop()
            self.queue.clear()

            return 'stopped playing audio'

        return 'currently not playing'

    async def leave(self):
        if self.client_status and self.client_status.voice_client and self.client_status.voice_client.is_connected():
            await self.client_status.voice_client.voice_disconnect()
            
            self.queue.clear()

            return None
        
        return 'currently not in a voice channel'
    
    def clear_queue(self):
        if self.client_status and self.client_status.voice_client and self.client_status.voice_client.is_connected():
            if len(self.queue) > 0:
                self.queue.clear()
                
                return 'queue cleared'
            
        return 'queue is already empty'
    
    async def skip(self):
        if not self.client_status or not self.client_status.voice_client or not self.client_status.voice_client.is_playing():
            return 'currently not playing'

        self.client_status.voice_client.stop()
        self.next_in_queue()

    def current_song(self):
        if len(self.queue) < 1:
            return None
        
        return self.queue[0]
    
    async def play(self, query: str, client_status: ClientStatus, followup: discord.Webhook):
        url_pattern = re.compile("/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/")
        url_no_prefix_pattern = re.compile("/^[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/")

        self.client_status = client_status

        if url_pattern.match(query) or url_no_prefix_pattern.match(query):
            pass
        else:
            youtube_entry = YoutubeEntry().search(query)
            if not youtube_entry:
                await followup.send(content="invalid video")
                return

            self.push(youtube_entry)

        if len(self.queue) < 1:
            await followup.send(content="internal error")
            return
        
        if self.client_status.voice_client.is_playing() or self.buffering:
            log(f'"{self.queue[-1].title}" pushed to queue')
            await followup.send(content=f'"{self.queue[-1].title}" pushed to queue')
            return
        
        Thread(name='play', target=self._play).start()
        
        await followup.send(content=f'"{self.queue[0].title}" now playing')
    
    @unsync
    async def next_in_queue(self, followup: discord.Webhook = None, from_transition = False):
        if self.transition:
            self.client_status.update_status()
            return
        
        # removes front of queue
        self.pop(0)

        if len(self.queue) < 1:
            self.client_status.update_status()
            return

        if followup:
            await followup.send(f'now playing {self.queue[0].title}')

        await self._play()

    def _play(self):
        log(f'buffering {self.queue[0].title}', 'w')

        self.buffering = True
        self.queue[0].fill_buffer(
            source = StreamExtractor().buffer(self.queue[0].url)
        )
        self.buffering = False

        log(f'now playing {self.queue[0].title}', 's')
        self.client_status.voice_client.play(source=discord.FFmpegOpusAudio(copy(self.queue[0].buffer),
                                                              before_options='',#'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                                              options=self._options(),
                                                              pipe=True, 
                                                              executable='ffmpeg/ffmpeg.exe'), 
                                after=lambda e: self.next_in_queue())
        
        self.queue[0].epoch = time.time()
        
    def _play_transition(self):
        log(f'transitioning {self.queue[0].title} to {self.queue[0].seek}', 'w')
        self.client_status.voice_client.play(source=discord.FFmpegOpusAudio(copy(self.queue[0].buffer),
                                                              before_options=f'-ss {self.queue[0].seek}',#'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                                              options=self._options(),
                                                              pipe=True, 
                                                              executable='ffmpeg/ffmpeg.exe'), 
                                after=lambda e: self.next_in_queue(from_transition=True))