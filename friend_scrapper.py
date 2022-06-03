from selenium import webdriver
from selenium.webdriver.common.by import By

__all__ = ['get_user_friends']

def get_user_friends(user: str) -> list[str]:
    driver = webdriver.Firefox()
    driver.get(f"https://myanimelist.net/profile/{user}")
    elements = driver.find_elements(By.CSS_SELECTOR, "a.icon-friend")
    friends = []
    for element in elements:
        friends.append(element.get_attribute("innerHTML"))
    driver.close()
    return friends

