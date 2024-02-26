from typing             import Dict
from threading          import Thread

import yt_dlp           as youtube_extractor

from helpers.discord    import *
from utilities.logs     import *

guild_data: Dict[int, GuildData]    = dict()

timeout_thread: Thread              = Thread(name='voice timeout', 
                                             target=timeout_handler)