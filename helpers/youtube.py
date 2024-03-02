from youtubesearchpython import VideosSearch, Playlist

import io

class YoutubeVideoData:
    def __init__(self, url: str = None, 
                 title: str = None, 
                 id: str = None, 
                 thumbnail: str = None, 
                 duration: str = None,
                 buffer: io.BytesIO = None):
        self.url = url
        self.title = title
        self.id = id
        self.thumbnail = thumbnail
        self.duration = duration
        self.buffer = buffer


class YoutubeEntry:
    def __init__(self):
        self.video_data     = YoutubeVideoData()
        self.query          = dict()

        self.entry_index    = 0

    def search(self, title: str):
        def __extract_thumbnail(url: str):
            return url[: url.find('?')]

        if self.entry_index > 2:
            return None
        
        self.query = title

        query = VideosSearch(title, limit=3)
        if not 'result' in query.result().keys() or len(list(query.result()['result'])) < self.entry_index + 1:
            return None

        query = query.result()['result']
        entry = query[self.entry_index]

        self.video_data = YoutubeVideoData(url=entry['link'],
                                           title=entry['title'],
                                           id=entry['id'],
                                           thumbnail=__extract_thumbnail(entry['thumbnails'][0]['url']),
                                           duration=entry['duration'])

        return self.video_data