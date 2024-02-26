from youtubesearchpython import VideosSearch, Playlist

import requests
import json

class VideoData:
    def __init__(self, url: str = None, 
                 title: str = None, 
                 id: str = None, 
                 thumbnail: str = None, 
                 duration: str = None):
        self.url = url
        self.title = title
        self.id = id
        self.thumbnail = thumbnail
        self.duration = duration


class YoutubeStream:
    def __init__(self):
        self.video_data = VideoData()

        self.api_host   = str()
        self.headers    = dict()
        self.options    = dict()


    def _request(self):
        def __setup_cobalt():
                self.api_host   = "https://co.wuk.sh/api/json"
                self.options    = { 
                    'aFormat':          'best',
                    'dubLang':          False,
                    'filenamePattern':  'classic',
                    'isAudioOnly':      True,
                    'isNoTTWatermark':  True,
                    'url':              ''
                }

                self.headers    = {
                    'Content-Type': 'application/json',
                    'Accept':       'application/json',
                    'User-Agent':   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
                }

        def __cobalt_extract_filename(headers: dict):
            content_disposition: str = headers['Content-disposition']
            filename = content_disposition[ content_disposition.find('"') + 1 : content_disposition.rfind('"') ]
            
            return filename
        
        def __cobalt_extract_filetype(headers: dict):
            content_type: str = headers['Content-Type']
            filetype = content_type[content_type.find('/') + 1 : ]

            return filetype
    
        __setup_cobalt()

        self.options['url'] = self.video_data.url

        response = requests.post(url=self.api_host, 
                                 headers=self.headers,
                                 data=json.dumps(self.options))
        
        response_body = response.json()

        self.headers['Accept'] = '*/*'
        self.headers.pop('Content-Type')
        response = requests.get(url=response_body['url'],
                                headers=self.headers)

        output = f'{__cobalt_extract_filename(response.headers)}.{__cobalt_extract_filetype(response.headers)}'
        with open(output, 'wb') as handle:
            handle.write(response.content)
            handle.close()

    def search(self, title: str):
        def __extract_thumbnail(url: str):
            return url[: url.find('?')]

        query = VideosSearch(title, limit=2)
        if not 'result' in query.result().keys() or len(list(query.result().keys())) <= 1:
            return False

        query = query.result()['result'][0]
        self.video_data = VideoData(url=query['link'],
                                    title=query['title'],
                                    id=query['id'],
                                    thumbnail=__extract_thumbnail(query['thumbnails'][0]['url']),
                                    duration=query['duration'])
        
        self._request()

        return True

stream = YoutubeStream()
stream.search('d79812gh8712hd97812hd798')