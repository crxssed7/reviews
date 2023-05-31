import requests
from .exceptions import APIException

BASE_URL = "https://graphql.anilist.co"

def request(query, variables):
    response = requests.post(BASE_URL, json={'query': query, 'variables': variables})
    if response.ok:
        data = response.json()
        return data["data"]
    raise APIException(f"[ANILIST:{response.status_code}] There was an error. Raw error: {response.json()}", response.status_code)

def get_manga(anilist_manga_id):
    query = '''
    query ($id: Int) {
      Media (id: $id, type: MANGA) {
        id
        title {
          romaji
          english
          native
        }
        startDate {
          year
          month
          day
        }
        status
        chapters
      }
    }
    '''

    variables = {
        'id': anilist_manga_id
    }

    data = request(query, variables)
    return data["Media"]
