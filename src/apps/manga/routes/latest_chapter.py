from flask import jsonify
from api import anilist, mangaupdates, exceptions

def manga_lastest_chapter(anilist_manga_id):
    try:
        anilist_data = None
        mangaupdates_data = None
        chapters = 0

        anilist_manga = anilist.get_manga(anilist_manga_id)
        if not anilist_manga:
            return jsonify({"error": "[ANILIST] Manga not found."}), 404
        anilist_manga = anilist_manga["Media"]

        anilist_data = {
            "title": anilist_manga["title"]["romaji"],
            "id": anilist_manga_id
        }

        if anilist_manga["status"] == "FINISHED":
            return jsonify(build_data(anilist_data, mangaupdates_data, anilist_manga["chapters"]))

        title = anilist_manga["title"]["romaji"]
        year = anilist_manga["startDate"]["year"]
        mangaupdates_manga = mangaupdates.search_manga(title, year)
        if not mangaupdates_manga:
            return jsonify({"error": "[MANGAUPDATES] Manga not found."}), 404

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

        return jsonify(build_data(anilist_data, mangaupdates_data, chapters))
    except exceptions.APIException as exception:
        return jsonify({"error": str(exception)}), exception.status_code

def build_data(anilist_data, mangaupdates_data, chapters):
    return {
        "anilist": anilist_data,
        "mangaupdates": mangaupdates_data,
        "chapters": chapters
    }

def isnum(record):
    value = record["record"]["chapter"]
    return str(value).isdigit()
