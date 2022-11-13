import requests
from bs4 import BeautifulSoup

__all__ = ['get_user_friends']


def get_user_friends(user: str) -> list[str]:
    data = requests.get(f"https://myanimelist.net/profile/{user}")
    soup = BeautifulSoup(data.text, 'html.parser')
    friends = []
    for element in soup.select('a.icon-friend'):
        friends.append(element.get('title'))
    return friends

