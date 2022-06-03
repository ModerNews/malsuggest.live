"""
Base score: 10
!! All of those are precise conditions, f.e. TOP 100 and TOP 50 do not exclude themselves !!
Scored 1 by one friend - -10
Scored 1 by 25% of watching friends - -10
Scored 1 by 100% of watching friends - -10

Scored 3 or less by one friend - -8
Scored 3 or less by 25% of watching friends - -5
Scored 3 or less by 100% of watching friends - -7

Scored 5 or less by one friend - -3
Scored 5 or less by 25% of watching friends - -3
Scored 5 or less by 100% of watching friends - -4

Scored 8 by one friend - +1
Scored 8 by 25% of watching friends - +2
Scored 8 by 100% of watching friends - +5

Scored 9 by one friend - +2
Scored 9 by 25% of watching friends - +4
Scored 9 by 100% of watching friends - +10

Scored 10 by one friend - +4
Scored 10 by 25% of watching friends - +8
Scored 10 by 100% of watching friends - +15

Watched by every of your friends - +5
To promote niche productions - watched by only 5% or less of your friends - +5

One of your favourite genres - +3
Three of your favourite genres - +10

On your ptw list - +3
Dropped by you - -10
Re-watched by any of your friends - +5

Is in MAL suggestions - +5

Is in TOP 100 - +3
Is in TOP 50 - + 3
Is in TOP 10 - + 4
Sums up to 10
"""
import math

import malclient
from friend_scrapper import *
from random import choice

from matplotlib import pyplot

print("Creating independent API connection...")


mal_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIzMDU5ZDA3NWY3NWYzMmEwZmY5YjgxMzYwMjBiZDZlZjBiMDUxYTk1YmU0NWFmMjQ2NDAxZGM4YjI0ODY5OWIzNDEzNzE1ODgwNDVkOTFhIn0.eyJhdWQiOiI0ODU2M2I5MDYzMTBkM2ZkYjRjZWZhMWMxODc3YmZjMyIsImp0aSI6IjIzMDU5ZDA3NWY3NWYzMmEwZmY5YjgxMzYwMjBiZDZlZjBiMDUxYTk1YmU0NWFmMjQ2NDAxZGM4YjI0ODY5OWIzNDEzNzE1ODgwNDVkOTFhIiwiaWF0IjoxNjUzODUwMjc3LCJuYmYiOjE2NTM4NTAyNzcsImV4cCI6MTY1NjUyODY3Nywic3ViIjoiMTA4MzEzMzAiLCJzY29wZXMiOltdfQ.agNWv5QUlC3T1XaH-MKBO7g0p6eSZ6LNjeNaBaYwifv_M1R4Q2QniKtlLtOJQuZguLe1GlOMq9qrklxVx99MlpfCdkVyNP2lSceBiB7UHrruRwmuwiHVW7qDjFA1QlpwvLYQNpFmmJD9AyLZcFnmhQ2yMH--wQUOUQYsH4EkmbDadJi3e8w1lNNtuI1Z1M1v9BQf0rjn1JGXY4AamHKrFj_gW8BgvYFu0N6hcnS6IxI_ebbapqQLfniW5RRfP6c8Ex684WBLH_bC5BjPc4e1GmDFk3OTfgLO5tijWQnK9i5UMpNVi1jWXylZRr7zQ0QYJcs6w-XBFQG9ps6-Eyp2PA'
client = malclient.Client(access_token=mal_access_token)

user_data = client.get_user_info()
friends = get_user_friends(user_data['name'])


friend_lists = []

print("Fetching list data for users: " + ", ".join(friends))

for user in friends:
    temp_list = client.get_user_anime_list(username=user, limit=1000, status='completed')['data'] + client.get_user_anime_list(username=user, limit=1000, status='watching')['data']
    friend_lists.append(temp_list)

total_animes = [item['id'] for sublist in friend_lists for item in sublist]
animes_watching = set([item["id"] for item in client.get_user_anime_list(status="watching")['data'] +
                       client.get_user_anime_list(status="on_hold")['data'] +
                       client.get_user_anime_list(status="completed")['data']])
animes_dropped = [item['id'] for item in client.get_user_anime_list(status="dropped")['data']]
animes_ptw = [item['id'] for item in client.get_user_anime_list(status="plan_to_watch")['data']]
total_unique_animes = {item: 10 for item in set(total_animes) - animes_watching}

animes_with_genres = {item: client.get_anime_details(item).genres for item in set(total_animes) - animes_watching}

animes_top_100 = [item.id for item in client.get_anime_ranking(limit=100)]
animes_top_50 = [item.id for item in client.get_anime_ranking(limit=50)]
animes_top_10 = [item.id for item in client.get_anime_ranking(limit=10)]
print("Filtering fetched data")

print(total_unique_animes.keys())

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

# region Deprecated
# dominant_wage = max(set(list(total_unique_animes.values())), key=list(total_unique_animes.values()).count)
# dominant_wage_count = list(total_unique_animes.values()).count(dominant_wage)
# custom_wages = list(total_unique_animes.values()).copy()
# ordered_wages = list(sorted(list(set(custom_wages.copy()))))
# for i in range(len(custom_wages)):
#     if custom_wages[i] > dominant_wage * 1.2:
#         # int(dominant_wage_count * (1 + dominant_wage_count/len(custom_wages))) *
#         custom_wages[i] *= ((len(ordered_wages) - ordered_wages.index(custom_wages[i]) + 1) ** 2)
#
# pyplot.figure(figsize=(19.2, 10.8))
# pyplot.scatter([-10 for i in range(len(total_unique_animes.values()))], list(total_unique_animes.values()), label="Rozkład domyślnych wag")
# test_data = [choices(list(total_unique_animes.values()), custom_wages)[0] for i in range(1000)]
# test_data_counts = [int(test_data.count(item)) for item in set(test_data)]
# test_data = list(set(test_data))
# pyplot.scatter(test_data_counts, test_data, label="Wybrane wartości wag")
#
# for i in range(len(test_data)):
#     pyplot.annotate(test_data_counts[i], (test_data_counts[i], test_data[i]))
#
# for i in range(len(set(total_unique_animes.values()))):
#     pyplot.annotate(list(total_unique_animes.values()).count(list(set(total_unique_animes.values()))[i]), (-10, list(set(total_unique_animes.values()))[i]))
#
# pyplot.yticks(range(-20, 36, 2))
# pyplot.grid()
# pyplot.xlabel("Ilość trafień w wartość (łącznych strzałów: 1000)")
# pyplot.ylabel("Wartość wagi przed modyfikacją")
# pyplot.legend()
# pyplot.show()
#
# data = choices(list(total_unique_animes.keys()), list(total_unique_animes.values()))
# anime_info = client.get_anime_details(data[0])
# print(total_unique_animes)
# print(anime_info.title, data[0], total_unique_animes[data[0]])
# endregion
