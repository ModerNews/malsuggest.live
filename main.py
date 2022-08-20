import library
from random import choice
import malclient

from friend_scrapper import get_user_friends

print("Creating independent API connection...")
app = library.App()
mal_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRhM2U5YzJiYmMyMmFmOTZhOGRhNDk3ZTkzZTk1MDQyZDlmMjUxNmU2NzY3NTY5YzUxNzFiOWZkNWQ4Y2ZiZjkyYTkxNGUyOGU4M2VhZWU1In0.eyJhdWQiOiJiYzIwODEwOTJiYTA1OWJiMDA2ZDYxMjkwMjg4NmRmYSIsImp0aSI6IjRhM2U5YzJiYmMyMmFmOTZhOGRhNDk3ZTkzZTk1MDQyZDlmMjUxNmU2NzY3NTY5YzUxNzFiOWZkNWQ4Y2ZiZjkyYTkxNGUyOGU4M2VhZWU1IiwiaWF0IjoxNjYwOTg2MTgyLCJuYmYiOjE2NjA5ODYxODIsImV4cCI6MTY2MzY2NDU4Miwic3ViIjoiMTA4MzEzMzAiLCJzY29wZXMiOltdfQ.TbsSo6OGO8l-z5grQBCBr7lljptfO2LETENQLfgfPr28x0y8oQrQfJ9Iku5KwzNWaYxtM64jvaaYQPpni59STQzyqYmcUY3xi6QXC4u6e8uQ1juvvcY_3SD7C6s-k49a3gGWaMUn59pPEH_rm3YykdBVMeb8hzRHa9AWkCMw6qLwUMyFrAUulgO2TcH0OOtLFm3J5rY8_oWmfW8LmGU2SrtYHk3vTJYV-OW7aLUpyQGXmrAqToiKKuF9MfDFwkJRbxfgrLRy_vx-PskK9q2RcAtCmX0-abaRugh3E39Dl9VPz_Xt8a73orfeKIX3tygfLxfRaJO7R9q1MJhhgdR9uA'
client = malclient.Client(access_token=mal_access_token)

user_data = client.get_user_info()
friends = get_user_friends(user_data['name'])

print("Fetching list data for users: " + ", ".join(friends))


app.populate_top_rankings(client)

merged_list, friend_lists = library.generate_friend_anime_list(client, friends)
animes_watching, animes_ptw, animes_dropped = library.get_client_status_lists(client)
animes_with_genres = library.generate_genre_list(merged_list, animes_watching)

total_unique_animes = library.generate_scores_table(merged_list, animes_watching)
total_unique_animes = library.calculate_genre_score(client, animes_with_genres, total_unique_animes.copy())
total_unique_animes = library.calculate_recommendation_score(client, total_unique_animes)
total_unique_animes = library.calculate_rewatch_score(merged_list, total_unique_animes)

total_anime_scores = library.get_friend_scores(friend_lists)
for anime, scores in total_anime_scores.items():
    try:
        total_unique_animes[anime] += library.calculate_friend_watch_rate_score(scores, friends)
        total_unique_animes[anime] += library.calculate_status_score(anime, animes_ptw, animes_dropped)
        total_unique_animes[anime] += library.calculate_rankings_score(anime, app.animes_top_100, app.animes_top_50, app.animes_top_10)
        total_unique_animes[anime] += library.calculate_friend_rating_score(app.pricing, scores)
    except KeyError:
        pass

max_value = max(total_unique_animes.values())
top_scored_animes = [key for key, value in total_unique_animes.items() if value == max_value]
print(top_scored_animes)
print(choice(top_scored_animes))
