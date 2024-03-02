import io

class AudioEntry:
    def __init__(self, 
                 title: str         = None, 
                 thumbnail: str     = None,
                 url: str           = None,
                 buffer: io.BytesIO = None):
        self.buffer: io.BytesIO         = buffer
        self.title: str                 = title
        self.url: str                   = url
        self.thumbnail: str             = thumbnail

        self.epoch                      = 0
        self.seek                       = 0

    def fill_buffer(self, source: io.BytesIO):
        self.buffer = source