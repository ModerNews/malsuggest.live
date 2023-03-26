import datetime
import os
import time

import jwt

from flask import Flask
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import malclient

from .database import Connector

__all__ = ["App"]


class DataBank(object):
    def __init__(self):
        # Recommendation system variables
        self.animes_top_100 = None
        self.animes_top_50 = None
        self.animes_top_10 = None
        self.pricing = {10: {1: 4, 0.25: 8, 0.99: 15},
                        9: {1: 1, 0.25: 2, 0.99: 5},
                        8: {1: 2, 0.25: 4, 0.99: 10},
                        5: {1: -3, 0.25: -3, 0.99: -4},
                        3: {1: -8, 0.25: -5, 0.99: -7},
                        1: {1: -10, 0.25: -10, 0.99: -10}}

    def populate_top_rankings(self, client):
        self.animes_top_100 = [item.id for item in client.get_anime_ranking(limit=100)]
        self.animes_top_50 = [item.id for item in client.get_anime_ranking(limit=50)]
        self.animes_top_10 = [item.id for item in client.get_anime_ranking(limit=10)]


class App(Flask):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name,
                         static_folder=os.getenv('STATIC_PATH', './static'),
                         template_folder=os.getenv('TEMPLATE_PATH', './templates'), *args, **kwargs)
        self.config.update(debug=True)
        self.debug_value = False

        # MAL variable
        self._private_client = None

        self.data_bank: DataBank = DataBank()

        self.database = None

        # self._jwt_private_key = serialization.load_pem_private_key(bytes(os.getenv('JWT_PRIVATE_KEY'), encoding="utf-8"), password=bytes(os.getenv('JWT_PASSWORD'), encoding='ascii'), backend=default_backend())

    def connect_private_malclient_instance(self):
        self._private_client = malclient.Client(client_id=os.getenv("MAL_CLIENT_ID"))

    def connect_database(self):
        self.database = Connector()

    def generate_session_token(self, user_id):
        return jwt.encode({"user_id": user_id, "created_at": time.mktime(datetime.datetime.now().timetuple())}, '2137', algorithm="HS256")