from flask import current_app
from . import celery, library

import os

from random import choice
import malclient

from .friend_scrapper import get_user_friends
from .database import Connector


@celery.task()
def awaited_debug():
    return True


def pass_data_to_database(data, task_id):
    connection = Connector()
    cache_id = connection.create_cache_data(*data)
    connection.bind_cache_to_task(task_id, cache_id)


@celery.task(bind=True)
def calculate_personal_score(self, client: malclient.Client, data_bank):
    """
    This Function calculates users score. This uses custom access token for each user, bypassing rate limit.
    """
    user_data = client.get_user_info()
    friends = get_user_friends(user_data.name)

    data_bank.populate_top_rankings(client)

    merged_list, friend_lists = library.generate_friend_anime_list(client, friends)
    animes_watching, animes_ptw, animes_dropped = library.get_client_status_lists(client)
    animes_with_genres = library.generate_genre_list(merged_list, animes_watching)

    total_unique_animes = library.generate_scores_table(merged_list, animes_watching, data_bank.animes_top_100)
    total_unique_animes = library.calculate_genre_score(client, animes_with_genres, total_unique_animes.copy())
    total_unique_animes = library.calculate_recommendation_score(client, total_unique_animes)
    total_unique_animes = library.calculate_rewatch_score(merged_list, total_unique_animes)

    total_anime_scores = library.get_friend_scores(friend_lists)
    for anime, scores in total_anime_scores.items():
        try:
            total_unique_animes[anime] += library.calculate_friend_watch_rate_score(scores, friends)
            total_unique_animes[anime] += library.calculate_status_score(anime, animes_ptw, animes_dropped)
            total_unique_animes[anime] += library.calculate_rankings_score(anime,
                                                                           data_bank.animes_top_100,
                                                                           data_bank.animes_top_50,
                                                                           data_bank.animes_top_10)
            total_unique_animes[anime] += library.calculate_friend_rating_score(data_bank.pricing, scores)
        except KeyError:
            pass

    top_scored_animes = [key for key, value in sorted(total_unique_animes.items(), key=lambda x: x[1], reverse=True)[:13]]
    # max_value = max(total_unique_animes.values())
    # top_scored_animes = [key for key, value in total_unique_animes.items() if value == max_value]
    chosen = choice(top_scored_animes)
    pass_data_to_database([top_scored_animes, chosen], self.request.id)
    return chosen
