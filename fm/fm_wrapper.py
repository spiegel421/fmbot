import time
import os
import logging
import json
from fm.fm_api import *


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
            top_artists = self.api.get_user_artists(user_name, limit=1)
            artist_count = top_artists.total_artists
            artists = self.api.get_user_artists(user_name, limit=1000).artists
            for artist in artists:
                if artist.name.lower() == artist_name.lower():
                    return artist.play_count
            return 0
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
