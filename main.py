
import datetime
import math
import time

import db_utils
import malclient
from friend_scrapper import *
from random import choice



print("Creating independent API connection...")


mal_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIzMDU5ZDA3NWY3NWYzMmEwZmY5YjgxMzYwMjBiZDZlZjBiMDUxYTk1YmU0NWFmMjQ2NDAxZGM4YjI0ODY5OWIzNDEzNzE1ODgwNDVkOTFhIn0.eyJhdWQiOiI0ODU2M2I5MDYzMTBkM2ZkYjRjZWZhMWMxODc3YmZjMyIsImp0aSI6IjIzMDU5ZDA3NWY3NWYzMmEwZmY5YjgxMzYwMjBiZDZlZjBiMDUxYTk1YmU0NWFmMjQ2NDAxZGM4YjI0ODY5OWIzNDEzNzE1ODgwNDVkOTFhIiwiaWF0IjoxNjUzODUwMjc3LCJuYmYiOjE2NTM4NTAyNzcsImV4cCI6MTY1NjUyODY3Nywic3ViIjoiMTA4MzEzMzAiLCJzY29wZXMiOltdfQ.agNWv5QUlC3T1XaH-MKBO7g0p6eSZ6LNjeNaBaYwifv_M1R4Q2QniKtlLtOJQuZguLe1GlOMq9qrklxVx99MlpfCdkVyNP2lSceBiB7UHrruRwmuwiHVW7qDjFA1QlpwvLYQNpFmmJD9AyLZcFnmhQ2yMH--wQUOUQYsH4EkmbDadJi3e8w1lNNtuI1Z1M1v9BQf0rjn1JGXY4AamHKrFj_gW8BgvYFu0N6hcnS6IxI_ebbapqQLfniW5RRfP6c8Ex684WBLH_bC5BjPc4e1GmDFk3OTfgLO5tijWQnK9i5UMpNVi1jWXylZRr7zQ0QYJcs6w-XBFQG9ps6-Eyp2PA'
client = malclient.Client(access_token=mal_access_token)

user_data = client.get_user_info()
friends = get_user_friends(user_data['name'])

db_client = db_utils.DatabaseClient("animes.db")

friend_lists = []

print("Fetching list data for users: " + ", ".join(friends))


def calculate_favourite_genres(user: str = "@me"):
    user_list = client.get_user_anime_list(username=user, limit=1000, status='completed', optional_fields=['genres'])['data']
    genres = {}
    total_count = len(user_list)
    for anime in user_list:
        try:
            for genre in anime['genres']:
                try:
                    genres[genre['name']]['count'] += 1
                    genres[genre['name']]['score'] += anime['score']
                except KeyError:
                    genres[genre['name']] = {'score': anime['score'], 'count': 1}
        except KeyError:
            pass
    # return sorted(genres.items(), key=lambda item: ((item[1]['score']/item[1]['count'])*45 + (item[1]['count']/total_count))/46, reverse=True)
    return sorted(genres.items(), key=lambda item: (item[1]['score'] + item[1]['count']/total_count)/(item[1]['count'] + 1), reverse=True)

for friend in friends:
    print(friend)
    for genre in calculate_favourite_genres(friend)[:10]:
        print(genre[0])
quit()

for user in friends:
    temp_list = client.get_user_anime_list(username=user, limit=1000, status='completed', optional_fields=["genres"])['data'] + client.get_user_anime_list(username=user, limit=1000, status='watching', optional_fields=["genres"])['data']
    friend_lists.append(temp_list)

merged_list = sum(friend_lists, [])

total_animes = [item['id'] for item in merged_list]
animes_watching = set([item["id"] for item in client.get_user_anime_list(status="watching")['data'] +
                       client.get_user_anime_list(status="on_hold")['data'] +
                       client.get_user_anime_list(status="completed")['data']])

animes_dropped = [item['id'] for item in client.get_user_anime_list(status="dropped")['data']]
animes_ptw = [item['id'] for item in client.get_user_anime_list(status="plan_to_watch")['data']]
total_unique_animes = {item: 10 for item in set(total_animes) - animes_watching}

# TODO This should be globalized, and synced just once in a while
animes_top_100 = [item.id for item in client.get_anime_ranking(limit=100)]
animes_top_50 = [item.id for item in client.get_anime_ranking(limit=50)]
animes_top_10 = [item.id for item in client.get_anime_ranking(limit=10)]
print("Filtering fetched data")

print(total_unique_animes.keys())

for item in merged_list:
    if item['is_rewatching']:
        try:
            total_unique_animes[item] += 5
        except KeyError:
            pass

animes_with_genres = {}

for item in merged_list:
    try:
        animes_with_genres[item["id"]] = [genre['name'] for genre in item["genres"]]
    except KeyError:
        print(f"{item['title']} has no genres")

print(animes_with_genres)


total_anime_scores: dict[int, list[int]] = {}
for user in friend_lists:
    for anime in user:
        if anime["id"] in total_anime_scores:
            total_anime_scores[anime["id"]].append(anime["score"])
        else:
            total_anime_scores[anime["id"]] = [anime["score"]]

# TODO check for correct values (UnitTest should be prepared)
pricing = {10: {1: 4, 0.25: 8, 0.99: 15},
           9: {1: 1, 0.25: 2, 0.99: 5},
           8: {1: 2, 0.25: 4, 0.99: 10},
           5: {1: -3, 0.25: -3, 0.99: -4},
           3: {1: -8, 0.25: -5, 0.99: -7},
           1: {1: -10, 0.25: -10, 0.99: -10}}

for anime, scores in total_anime_scores.items():
    if len(scores) == len(friends):
        try:
            total_unique_animes[anime] += 5
        except KeyError:
            pass
    elif len(scores) <= math.ceil(len(friends)*0.05):
        try:
            total_unique_animes[anime] += 5
        except KeyError:
            pass

    if anime in animes_ptw:
        try:
            total_unique_animes[anime] += 3
        except KeyError:
            pass
    elif anime in animes_dropped:
        try:
            total_unique_animes[anime] -= 10
        except KeyError:
            pass

    if anime in animes_top_100:
        try:
            total_unique_animes[anime] += 3
        except KeyError:
            pass
    if anime in animes_top_50:
        try:
            total_unique_animes[anime] += 3
        except KeyError:
            pass
    if anime in animes_top_10:
        try:
            total_unique_animes[anime] += 4
        except KeyError:
            pass

    for score in (10, 9, 8, 5, 3, 1):
        for value, price in pricing[score].items():
            if isinstance(value, float):
                if scores.count(score) > len(scores) * value:
                    try:
                        total_unique_animes[anime] += price
                    except KeyError:
                        pass
            else:
                if scores.count(score) > value:
                    try:
                        total_unique_animes[anime] += price
                    except KeyError:
                        pass

max_value = max(total_unique_animes.values())
top_scored_animes = [key for key, value in total_unique_animes.items() if value == max_value]
print(choice(top_scored_animes))
