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
volumes
coverImage {
    extraLarge
    large
    medium
    color
}
bannerImage
description
tags {
    name
}
genres
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
entries {
  %LIST_DATA%
}
""".replace("%LIST_DATA%", LIST_DATA)

LIST_COLLECTION_DATA = """
lists {
    %LIST_GROUP_DATA%
}
""".replace("%LIST_GROUP_DATA%", LIST_GROUP_DATA)

def get_data(data, anilist_type):
    return None if data is None else data[anilist_type]

def request(query, variables, safe = False):
    response = requests.post(BASE_URL, json={'query': query, 'variables': variables})
    if response.ok:
        data = response.json()
        return data["data"]
    if safe:
        return None
    raise APIException(f"[ANILIST:{response.status_code}] There was an error. Raw error: {response.json()}", response.status_code)

def get_manga(anilist_manga_id, safe = False):
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

    data = request(query, variables, safe=safe)
    return get_data(data, "Media")

def get_media_list(anilist_manga_id, user_id, safe = False):
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

    data = request(query, variables, safe=safe)
    return get_data(data, "MediaList")

def get_media_list_collection(user_id, sort_fields, safe = False):
    query = """
    query ($userId: Int, $sort: [MediaListSort]) {
      MediaListCollection(userId: $userId, type: MANGA, sort: $sort) {
        %LIST_COLLECTION_DATA%
      }
    }
    """.replace("%LIST_COLLECTION_DATA%", LIST_COLLECTION_DATA)

    variables = {
        "userId": user_id,
        "sort": sort_fields
    }

    data = request(query, variables, safe=safe)
    return get_data(data, "MediaListCollection")

def get_review(user_id, anilist_manga_id, safe = False):
    query = """
    query ($userId: Int, $mediaId: Int) {
        Review(userId: $userId, mediaId: $mediaId) {
		    body
            summary
        }
    }
    """

    variables = {
        "userId": user_id,
        "mediaId": anilist_manga_id
    }

    data = request(query, variables, safe=safe)
    return get_data(data, "Review")
