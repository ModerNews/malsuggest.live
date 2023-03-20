import math
import malclient


class App(object):
    def __init__(self):
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


def calculate_favourite_genres(client, user: str = "@me"):
    fields = malclient.Fields()
    fields.genres = True
    # fields.list_status = malclient.ListStatusFields.all()
    user_list = client.get_user_anime_list(username=user, limit=1000, status='completed', fields=fields, list_status_fields=malclient.ListStatusFields.all())
    genres = {}
    total_count = len(user_list)
    for anime in user_list:
        try:
            for genre in anime.genres:
                try:
                    genres[genre.name]['count'] += 1
                    genres[genre.name]['score'] += anime.list_status.score
                except KeyError:
                    genres[genre.name] = {'score': anime.list_status.score, 'count': 1}
        except TypeError:
            pass
    return sorted(genres.items(),
                  key=lambda item: (item[1]['score'] + item[1]['count'] / total_count) / (item[1]['count'] + 1),
                  reverse=True)


def calculate_genre_score(client, anime_list: dict, score_list: dict[int, int]):
    favourite_genres = [genre[0] for genre in calculate_favourite_genres(client)[:10]]
    for anime, genres in anime_list.items():
        genre_score = sum([1 if genre in favourite_genres else 0 for genre in genres])
        if genre_score >= 3:
            score_list[anime] += 3
        if genre_score >= 5:
            score_list[anime] += 10
    return score_list


def calculate_recommendation_score(client, score_list: dict[int, int]):
    suggestions = [item.id for item in client.get_suggested_anime()]
    for anime, score in score_list.items():
        if anime in suggestions:
            score_list[anime] += 5
    return score_list


def generate_friend_anime_list(client, friends):
    friend_lists = []
    for user in friends:
        # fields = malclient.Fields()
        # fields.genres, fields.related_anime, fields.related_manga = True, malclient.Fields().node(), malclient.Fields().node()
        fields = ["genres", "related_anime", "related_manga"]
        temp_list1 = client.get_user_anime_list(username=user, limit=1000, status='completed', fields=malclient.Fields.from_list(fields), list_status_fields=malclient.ListStatusFields.all())
        temp_list2 = client.get_user_anime_list(username=user, limit=1000, status='watching', fields=malclient.Fields.from_list(fields), list_status_fields=malclient.ListStatusFields.all())
        friend_lists.append(temp_list1 if temp_list1 else [] + temp_list2 if temp_list2 else [])

    return sum(friend_lists, []), friend_lists


def get_client_status_lists(client):
    tmp1 = client.get_user_anime_list(status="watching")
    tmp2 = client.get_user_anime_list(status="on_hold")
    tmp3 = client.get_user_anime_list(status="completed")

    animes_watching = set([item.id for item in [tmp1 if tmp1 else [] + tmp2 if tmp2 else [] + tmp3 if tmp3 else []][0]])

    animes_dropped = [item.id for item in client.get_user_anime_list(status="dropped")]
    animes_ptw = [item.id for item in client.get_user_anime_list(status="plan_to_watch")]
    return animes_watching, animes_ptw, animes_dropped


def generate_scores_table(anime_list, animes_watching):
    return {item: 10 for item in set([item.id for item in anime_list]) - animes_watching}


def calculate_rewatch_score(merged_list, anime_score_list):
    for item in merged_list:
        if item.list_status.is_rewatching:
            try:
                anime_score_list[item.id] += 5
            except KeyError:
                pass
    return anime_score_list


def get_friend_scores(friend_lists):
    total_anime_scores: dict[int, list[int]] = {}
    for user in friend_lists:
        for anime in user:
            if anime.id in total_anime_scores:
                total_anime_scores[anime.id].append(anime.list_status.score)
            else:
                total_anime_scores[anime.id] = [anime.list_status.score]
    return total_anime_scores


def calculate_friend_watch_rate_score(scores, friends):
    change = 0
    if len(scores) == len(friends):
        change = 5
    elif len(scores) <= math.ceil(len(friends) * 0.05):
        change = 5
    return change


def calculate_status_score(anime, animes_ptw, animes_dropped):
    change = 0
    if anime in animes_ptw:
        change = 3
    elif anime in animes_dropped:
        change = -10
    return change


def calculate_rankings_score(anime, top_100, top_50, top_10):
    change = 0
    if anime in top_100:
        change += 3
    if anime in top_50:
        change += 3
    if anime in top_10:
        change += 4
    return change


def calculate_friend_rating_score(pricing, scores):
    change = 0
    for score in (10, 9, 8, 5, 3, 1):
        for value, price in pricing[score].items():
            if isinstance(value, float):
                if scores.count(score) > len(scores) * value:
                    try:
                        change += price
                    except KeyError:
                        pass
            else:
                if scores.count(score) > value:
                        change += price
    return change


def generate_genre_list(merged_list, animes_watching):
    animes_with_genres = {}
    for item in merged_list:
        if item.id in animes_watching:
            continue
        try:
            animes_with_genres[item.id] = [genre.name for genre in item.genres]
        except TypeError:
            print(f"{item.title} has no genres")
    return animes_with_genres