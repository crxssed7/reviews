from flask import render_template

from api.anilist import get_media_list_collection
from api.presenters import MediaListCollectionPresenter
from helpers import USER_ID

def manga_index():
    media_list_collection = get_media_list_collection(USER_ID, ["UPDATED_TIME_DESC"])
    presenter = MediaListCollectionPresenter(media_list_collection)
    reading = presenter.get_status("CURRENT").entries
    completed = presenter.get_status("COMPLETED").sort_by("completed_at", reverse=True).entries
    paused = presenter.get_status("PAUSED").entries
    planning = presenter.get_status("PLANNING").sort_by("priority", reverse=True).entries
    len_reading = len(reading)
    len_completed = len(completed)
    len_paused = len(paused)
    len_planning = len(planning)
    return render_template("manga_index.html", reading=reading, completed=completed, paused=paused, planning=planning, len_reading=len_reading, len_completed=len_completed, len_paused=len_paused, len_planning=len_planning)
