from helpers.entry import *
from helpers.youtube import YoutubeVideoData

from typing import Dict, List

class AudioQueue:
    def __init__(self):
        self.modifiers: Dict = dict()
        self.queue: List[AudioEntry] = list()

        self.update_modifiers()

    def update_modifiers(self, pitch: float = 1, tempo: float = 1, bass: float = 0):
        self.modifiers = {
            'pitch': pitch,
            'tempo': tempo,
            'bass': bass
        }

    def push(self, entry):
        if type(entry) == YoutubeVideoData:
            entry: YoutubeVideoData
            self.queue.append(AudioEntry(title=entry.title,
                                         thumbnail=entry.thumbnail,
                                         buffer=entry.buffer))
            
            return
        
        self.queue.append(entry)

    def pop(self, index = None):
        self.queue.pop(index) if index else self.queue.pop()

    def current_song(self):
        if len(self.queue) < 1:
            return None
        
        return self.queue[0]