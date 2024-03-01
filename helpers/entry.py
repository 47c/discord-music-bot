import io

class AudioEntry:
    def __init__(self, 
                 title: str = None, 
                 thumbnail: str = None,
                 buffer: io.BytesIO = None):
        self.buffer: io.BytesIO = buffer
        self.title: str = title
        self.thumbnail: str = thumbnail