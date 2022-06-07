import time

import malclient
import sqlite3


def update_top_anime_data(client: malclient.Client, *, limit: int = 500):
    assert limit <= 500
    top_data = [item.id for item in client.get_anime_ranking(limit=limit)]
    animes_with_genres = {}
    for data in top_data:
        try:
            animes_with_genres[data] = client.get_anime_genres(data)
        except malclient.Forbidden:
            time.sleep(10)

    with sqlite3.connect('../animes.db') as connection:
        cursor = connection.cursor()
        for anime, genres in animes_with_genres.items():
            cursor.execute("INSERT INTO genres VALUES (?, ? )", (anime, ",".join([genre.name for genre in genres])))
        connection.commit()