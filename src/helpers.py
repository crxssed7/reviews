from api.exceptions import APIException
from api.mangaupdates import search_manga, search_releases

def isnum(record):
    value = record["record"]["chapter"]
    return str(value).isdigit()

def latest_chapter_by_anilist(anilist_media):
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

        # TODO: Cache these results

        return chapters, mangaupdates_data
    except APIException:
        return 0, None