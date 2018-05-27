import time
import os
import logging
import json
from lastfm_api import *


class LastFmWrapper:
    def __init__(self):
        logging.info("Initializing Last.fm...")
        self.api = LastfmAPI()

    def get_last_played(self, user_name):
        try:
            recent_tracks = self.api.get_recent_tracks(user_name,limit=1)
            if len(recent_tracks) > 0:
                return recent_tracks[0]
        except:
            return None

    def get_recent_tracks(self, user_name, limit=1000):
        try:
            recent_tracks = self.api.get_recent_tracks(user_name, limit=limit)
            if len(recent_tracks) > 0:
                return recent_tracks
            else:
                return None
        except:
            return None

    def get_user_numscrobbles(self, user_name, artist_name):
        try:
            num_scrobbles = self.api.get_num_scrobbles(user_name, artist_name)
            return num_scrobbles
        except:
            return 0


    def get_user(self, user_name):
        try:
            return self.api.get_user_info(user_name)
        except:
            return None

    def get_user_artistcount(self, user_name):
        try:
            return self.api.get_user_artists(user_name, limit=1).total_artists
        except:
            return 0

    def get_user_albumcount(self, user_name):
        try:
            return self.api.get_user_albums(user_name, limit=1).total_albums
        except:
            return 0


    def get_user_artists(self, user_name, limit=None):
        try:
            return self.api.get_user_artists(user_name,limit)
        except:
            return None

    def get_user_albums(self, user_name, limit=None):
        try:
            return self.api.get_user_albums(user_name, limit)
        except:
            return None

    def get_user_tags(self, user_name):
        try:
            return self.api.get_user_tags(user_name)
        except:
            return None
