from .models import MangaObject, Node

__manga_fields__ = [
            "id",
            "title",
            "main_picture",
            "alternative_titles",
            "start_date",
            "end_date",
            "synopsis",
            "mean",
            "rank",
            "popularity",
            "num_list_users",
            "num_scoring_users",
            "nsfw,created_at",
            "updated_at",
            "media_type,status",
            "genres",
            "my_list_status",
            "num_volumes",
            "num_chapters",
            "authors{first_name,last_name}",
            "pictures",
            "background",
            "related_anime",
            "related_manga",
            "recommendations",
        ]


class Manga:
    def __init__(self):
        return

    def search_manga(self, keyword: str, limit: int = 20, nsfw: bool = None, manga_fields=None) -> list[Node]:
        """
        Lookup manga with keyword phrase on https://myanimelist.net

        :param keyword: string to look by
        :param limit: number of queries returned
        :param nsfw: boolean enabling/disabling nsfw filter

        :returns: list of manga Node objects
        :rtype: list[Node]
        """
        if nsfw is None:
            nsfw = self.nsfw
        uri = 'manga'
        params = {
            "q": keyword,
            "limit": limit,
            "fields": ','.join(__manga_fields__),
            'nsfw': nsfw
        }
        return [Node(**temp_object) for temp_object in self._api_handler.call(uri, params=params)["data"]]

    def get_manga_details(self, manga_id):
        """
        Get full info about manga with provided id

        :param id: id on https://myanimelist.net

        :returns: MangaObject for requested id
        :rtype: MangaObject
        """
        uri = f'manga/{manga_id}'
        params = {"fields": ','.join(__manga_fields__)}
        data = self._api_handler.call(uri, params=params)
        return MangaObject(**data)

    # TODO objectify manga ranking
    def get_manga_ranking(self, ranking_type="manga", limit=20):
        uri = 'manga/ranking'
        ranking_types = [
            "novels", "oneshots", "doujin", "manhwa", "manhua", "bypopularity",
            "favorite"
        ]

        if ranking_type not in ranking_types:
            return
        params = {
            "ranking_type": ranking_type,
            "limit": limit,
            "fields": ','.join(self.manga_fields)
        }
        return self._api_handler.call(uri, params)
