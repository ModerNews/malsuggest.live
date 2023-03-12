import os


from src.app import library
from random import choice
import malclient

from src.app.friend_scrapper import get_user_friends

print("Creating independent API connection...")
app = library.App()
client = malclient.Client(access_token=os.getenv('MAL_ACCESS'))

user_data = client.get_user_info()
friends = get_user_friends(user_data.name)

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
