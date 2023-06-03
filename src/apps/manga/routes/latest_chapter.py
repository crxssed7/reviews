from flask import jsonify
from api import anilist, mangaupdates, exceptions, presenters

# TODO: Extract and refactor this file

def latest_chapter(media):
    try:
        chapters = 0
        title = media.romaji
        year = media.start_date["year"]
        mangaupdates_manga = mangaupdates.search_manga(title, year)
        if not mangaupdates_manga:
            return 0, None
        mangaupdates_data = {
            "title": mangaupdates_manga["title"],
            "id": mangaupdates_manga["series_id"]
        }

        releases = mangaupdates.search_releases(
            str(mangaupdates_manga["series_id"]),
            "date",
            "desc"
        )
        filtered_results = list(filter(isnum, releases))
        if len(filtered_results) > 0:
            chapters = max(int(r["record"]["chapter"]) for r in filtered_results)

        # TODO: Cache these results

        return chapters, mangaupdates_data
    except exceptions.APIException:
        return 0, None

def manga_lastest_chapter(anilist_manga_id):
    anilist_data = None
    mangaupdates_data = None
    chapters = 0

    try:
        anilist_manga = anilist.get_manga(anilist_manga_id)
        anilist_data = {
            "title": anilist_manga["title"]["romaji"],
            "id": anilist_manga_id
        }
    except exceptions.APIException as exception:
        return jsonify({"error": str(exception)}), exception.status_code

    media = presenters.MediaPresenter(anilist_manga)

    if media.status == "FINISHED":
        return jsonify(build_data(anilist_data, mangaupdates_data, media.chapters))

    chapters, mangaupdates_data = latest_chapter(media)

    return jsonify(build_data(anilist_data, mangaupdates_data, chapters))


def build_data(anilist_data, mangaupdates_data, chapters):
    return {
        "anilist": anilist_data,
        "mangaupdates": mangaupdates_data,
        "chapters": chapters
    }

def isnum(record):
    value = record["record"]["chapter"]
    return str(value).isdigit()
