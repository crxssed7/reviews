from dotenv import dotenv_values
from flask import current_app

from api.anilist import get_review
from api.exceptions import APIException
from api.mangaupdates import search_manga, search_releases

ENV = dotenv_values()

USER_ID = ENV.get("USER_ID", "5613718")
USER_NAME = ENV.get("USER_NAME")
USER_AVATAR = ENV.get("USER_AVATAR", "https://s4.anilist.co/file/anilistcdn/user/avatar/large/default.png")
DEBUG = ENV.get("REVIEWS_DEBUG", "False").lower() in ("true", "1", "t")

STATUSES = {
    "reading": "CURRENT",
    "completed": "COMPLETED",
    "planning": "PLANNING",
    "paused": "PAUSED"
}

AL_STATUSES = { STATUSES[k]:k for k in STATUSES}

def isnum(record):
    value = record["record"]["chapter"]
    return str(value).isdigit()

def get_cached_latest_chapter(anilist_media):
    return current_app.cache.get(f"{anilist_media.id}.latest_chapter")

def latest_chapter_by_anilist(anilist_media):
    cache = current_app.cache

    existing_cache = get_cached_latest_chapter(anilist_media)
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

def get_review_content(presenter):
    if presenter.is_current() and presenter.media.is_finished():
        # Don't bother getting reviews for a currently reading finished manga
        return "I'm currently reading this manga, so I haven't written a review yet."

    cache = current_app.cache

    existing_review_cache = cache.get(f"{presenter.media.id}.review")
    if existing_review_cache:
        return existing_review_cache

    review = get_review(USER_ID, presenter.media.id, safe=True)
    if review:
        return review["body"]

    return presenter.notes if presenter.notes else "I haven't written a review for this manga yet."
