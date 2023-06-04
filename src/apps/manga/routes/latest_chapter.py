from flask import jsonify
from api import anilist, exceptions, presenters
from helpers import latest_chapter_by_anilist

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

    chapters, mangaupdates_data = latest_chapter_by_anilist(media)

    return jsonify(build_data(anilist_data, mangaupdates_data, chapters))


def build_data(anilist_data, mangaupdates_data, chapters):
    return {
        "anilist": anilist_data,
        "mangaupdates": mangaupdates_data,
        "chapters": chapters
    }
