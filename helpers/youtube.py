import requests
import json

class YoutubeStream:
    def __init__(self):
        self.url        = "https://www.youtube.com/watch?v=w4oHzLvKB9o"

        self.api_host   = str()
        self.headers    = dict()
        self.options    = dict()

    def __setup_cobalt(self):
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

    def __cobalt_extract_filename(self, headers: dict):
        content_disposition: str = headers['Content-disposition']
        filename = content_disposition[ content_disposition.find('"') + 1 : content_disposition.rfind('"') ]
        
        return filename
    
    def __cobalt_extract_filetype(self, headers: dict):
        content_type: str = headers['Content-Type']
        filetype = content_type[content_type.find('/') + 1 : ]

        return filetype

    def _request(self):
        self.__setup_cobalt()

        self.options['url'] = self.url

        response = requests.post(url=self.api_host, 
                                 headers=self.headers,
                                 data=json.dumps(self.options))
        
        response_body = response.json()

        self.headers['Accept'] = '*/*'
        self.headers.pop('Content-Type')
        response = requests.get(url=response_body['url'],
                                headers=self.headers)

        output = f'{self.__cobalt_extract_filename(response.headers)}.{self.__cobalt_extract_filetype(response.headers)}'
        with open(output, 'wb') as handle:
            handle.write(response.content)
            handle.close()

stream = YoutubeStream()
stream._request()