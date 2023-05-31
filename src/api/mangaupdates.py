import requests
from .exceptions import APIException

BASE_URL = "https://api.mangaupdates.com/v1/"

def request(endpoint, **data):
    response = requests.post(f"{BASE_URL}{endpoint}", json=data)

    if response.ok:
        json = response.json()
        return json
    raise APIException(f"[MANGAUPDATES:{response.status_code}] There was an error. Raw error: {response.json()}", response.status_code)

def search_manga(title, year):
    data = request("series/search", search=title, stype="title", year=year)

    if len(data["results"]) > 0:
        return data["results"][0]["record"]
    return None

def search_releases(manga_updates_id, orderby, sort):
    data = request("releases/search", search=manga_updates_id, search_type="series", orderby=orderby, asc=sort)
    return data["results"]
