from flask import current_app

from api.exceptions import APIException
from api.mangaupdates import search_manga, search_releases

# TODO: Move to dotenv
USER_ID = 5613718

def isnum(record):
    value = record["record"]["chapter"]
    return str(value).isdigit()

def latest_chapter_by_anilist(anilist_media):
    cache = current_app.cache

    existing_cache = cache.get(f"{anilist_media.id}.latest_chapter")
    if existing_cache:
        return existing_cache["chapters"], existing_cache["data"]

    try:
        chapters = 0
        title = anilist_media.romaji
        year = anilist_media.start_date["year"]
        mangaupdates_manga = search_manga(title, year)
        if not mangaupdates_manga:
            return 0, None
        mangaupdates_data = {
            "title": mangaupdates_manga["title"],
            "id": mangaupdates_manga["series_id"]
        }

        releases = search_releases(
            str(mangaupdates_manga["series_id"]),
            "date",
            "desc"
        )
        filtered_results = list(filter(isnum, releases))
        if len(filtered_results) > 0:
            chapters = max(int(r["record"]["chapter"]) for r in filtered_results)

        new_cache = {
            "chapters": chapters,
            "data": mangaupdates_data
        }
        cache.set(f"{anilist_media.id}.latest_chapter", new_cache)

        return chapters, mangaupdates_data
    except APIException:
        return 0, None
