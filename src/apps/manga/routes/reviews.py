from flask import render_template

from api.anilist import get_media_list
from api.exceptions import APIException

def manga_review(anilist_manga_id):
    try:
        media_list = get_media_list(anilist_manga_id, 5613718)
        return render_template("manga_review.html", media_list=media_list)
    except APIException as exception:
        return "Not found", exception.status_code
