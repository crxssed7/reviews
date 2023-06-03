import requests
from .exceptions import APIException

BASE_URL = "https://graphql.anilist.co"

MEDIA_DATA = """
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
coverImage {
    extraLarge
    large
    medium
    color
}
bannerImage
"""

LIST_DATA = """
id
priority
customLists
progress
updatedAt
completedAt {
    year
    month
    day
}
startedAt {
    year
    month
    day
}
notes
score
status
media {
    %MEDIA_DATA%
}
""".replace("%MEDIA_DATA%", MEDIA_DATA)

LIST_GROUP_DATA = """
name
isCustomList
isSplitCompletedList
status
name
entries {
  %LIST_DATA%
}
""".replace("%LIST_GROUP_DATA%", LIST_DATA)

def request(query, variables):
    response = requests.post(BASE_URL, json={'query': query, 'variables': variables})
    if response.ok:
        data = response.json()
        return data["data"]
    raise APIException(f"[ANILIST:{response.status_code}] There was an error. Raw error: {response.json()}", response.status_code)

def get_manga(anilist_manga_id):
    query = """
    query ($id: Int) {
      Media (id: $id, type: MANGA) {
        %MEDIA_DATA%
      }
    }
    """.replace("%MEDIA_DATA%", MEDIA_DATA)

    variables = {
        "id": anilist_manga_id
    }

    data = request(query, variables)
    return data["Media"]

def get_media_list(anilist_manga_id, user_id):
    query = """
    query ($userId: Int, $mediaId: Int) {
      MediaList(userId: $userId, mediaId: $mediaId) {
        %LIST_DATA%
      }
    }
    """.replace("%LIST_DATA%", LIST_DATA)

    variables = {
        "mediaId": anilist_manga_id,
        "userId": user_id
    }

    data = request(query, variables)
    return data["MediaList"]

# def get_media_list_group(status, user_id):
#     query = """
#     query ($userId: Int, $mediaId: Int) {
#       MediaList(userId: $userId, mediaId: $mediaId) {
#         %LIST_DATA%
#       }
#     }
#     """.replace("%LIST_DATA%", LIST_DATA)

#     variables = {
#         "mediaId": anilist_manga_id,
#         "userId": user_id
#     }

#     data = request(query, variables)
#     return data["MediaList"]
