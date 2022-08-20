import sqlite3
import time

import malclient
from utility import update_top_anime_data
import requests
import logging
import os

class App(object):
    def __init__(self):
        logging.basicConfig(format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d - %(message)s",
                            level=logging.INFO)
        logging.info("Fetching data about top 1000 entries")
        self.cached_anime = [anime.id for anime in client.get_anime_ranking(limit=500)] + [anime.id for anime in client.get_anime_ranking(limit=500, offset=500)]

logging.info("Connecting to API interface")
mal_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIzMDU5ZDA3NWY3NWYzMmEwZmY5YjgxMzYwMjBiZDZlZjBiMDUxYTk1YmU0NWFmMjQ2NDAxZGM4YjI0ODY5OWIzNDEzNzE1ODgwNDVkOTFhIn0.eyJhdWQiOiI0ODU2M2I5MDYzMTBkM2ZkYjRjZWZhMWMxODc3YmZjMyIsImp0aSI6IjIzMDU5ZDA3NWY3NWYzMmEwZmY5YjgxMzYwMjBiZDZlZjBiMDUxYTk1YmU0NWFmMjQ2NDAxZGM4YjI0ODY5OWIzNDEzNzE1ODgwNDVkOTFhIiwiaWF0IjoxNjUzODUwMjc3LCJuYmYiOjE2NTM4NTAyNzcsImV4cCI6MTY1NjUyODY3Nywic3ViIjoiMTA4MzEzMzAiLCJzY29wZXMiOltdfQ.agNWv5QUlC3T1XaH-MKBO7g0p6eSZ6LNjeNaBaYwifv_M1R4Q2QniKtlLtOJQuZguLe1GlOMq9qrklxVx99MlpfCdkVyNP2lSceBiB7UHrruRwmuwiHVW7qDjFA1QlpwvLYQNpFmmJD9AyLZcFnmhQ2yMH--wQUOUQYsH4EkmbDadJi3e8w1lNNtuI1Z1M1v9BQf0rjn1JGXY4AamHKrFj_gW8BgvYFu0N6hcnS6IxI_ebbapqQLfniW5RRfP6c8Ex684WBLH_bC5BjPc4e1GmDFk3OTfgLO5tijWQnK9i5UMpNVi1jWXylZRr7zQ0QYJcs6w-XBFQG9ps6-Eyp2PA'
client = malclient.Client(access_token=mal_access_token)

franchises = {}

for i in range(len(top_anime)):
    logging.info(f'Fetching data for anime {top_anime[i]} - {i}/{len(top_anime)}')
    while True:
        try:
            time.sleep(1)
            temp_data = client.get_anime_details(top_anime[i])
            franchises[top_anime[i]] = {}
            if temp_data.related_anime:
                franchises[top_anime[i]]['anime'] = [{"id": anime.node.id, "relation": anime.relation_type} for anime in temp_data.related_anime]
                franchises[top_anime[i]]['manga'] = [{"id": manha.node.id, "relation": manha.relation_type} for manha in temp_data.related_manga]
                logging.info(f'Fetch successful')
        except malclient.Forbidden:
            logging.warning("Forbidden - app was timedout, retrying in 60s")
            time.sleep(60)
            continue
        break

logging.info("Finished fetching, starting database push")
print(franchises)
connection = sqlite3.Connection("../animes.db")
cursor = connection.cursor()
i = 0
for entry, data in franchises.items():
    logging.info(f"Now pushing {i}/{len(franchises.items())}")
    for key, value in data.items():
        parsed_data = {
            "sequels": [], "prequels": [], "alternative_setting": [], "alternative_version": [], "side_story": [],
            "parent_story": [], "full_story": [], "summary": [], "unknown": []}
        for relation in value:
            try:
                parsed_data[relation["relation"]].append(relation['id'])
            except KeyError:
                parsed_data["unknown"].append(relation['id'])
        logging.info(f"Generated data for `{entry}/related_{key}`")
        helper = [",".join([str(temp) for temp in relation_type]) for relation_type in parsed_data.values()]
        cursor.execute(f"INSERT INTO {str(key)}_relations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple([entry] + helper))
        connection.commit()
        logging.info(f"Successfully appended data for `{entry}/related_{key}`")
    i += 1
requests.post('https://discord.com/api/webhooks/939865229666431017/nNTS6H3rYAwe8-yeFZYcos-6VSNSgiC8KiDaYwfJke5CCG4c9TDjg-WoSKMT6RjjgKke', json={"content": "<@!287258679609393152> zrobione!"}, headers={'Content-Type': 'application/json'})
logging.info("Script finished successfully, processing to sleep in 60s")
time.sleep(60)
os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")