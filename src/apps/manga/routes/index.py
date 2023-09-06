from flask import render_template, redirect

from api.anilist import get_media_list_collection
from api.presenters import MediaListCollectionPresenter
from helpers import USER_ID, STATUSES

def status(status):
    al_status = STATUSES.get(status)
    if not al_status:
        return "Not found", 404

    media_list_collection = get_media_list_collection(USER_ID, ["UPDATED_TIME_DESC"])
    presenter = MediaListCollectionPresenter(media_list_collection)
    entries = presenter.get_status(al_status).entries
    entry_count = len(entries)

    len_reading = len(presenter.get_status("CURRENT").entries)
    len_completed = len(presenter.get_status("COMPLETED").sort_by("completed_at", reverse=True).entries)
    len_paused = len(presenter.get_status("PAUSED").entries)
    len_planning = len(presenter.get_status("PLANNING").sort_by("priority", reverse=True).entries)
    total_manga = len_reading + len_completed + len_planning + len_paused
    percent_reading = (len_reading / total_manga) * 100
    percent_completed = (len_completed / total_manga) * 100
    percent_planning = (len_planning / total_manga) * 100
    percent_paused = (len_paused / total_manga) * 100

    return render_template(
        "manga_index.html",
        status=status,
        entries=entries,
        entry_count=entry_count,
        percent_reading=percent_reading,
        percent_completed=percent_completed,
        percent_paused=percent_paused,
        percent_planning=percent_planning
    )

def manga_index():
    return redirect("/reading", code=302)
