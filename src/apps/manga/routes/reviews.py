from datetime import date
from flask import render_template, current_app

from api.anilist import get_media_list
from api.exceptions import APIException
from api.presenters import MediaListPresenter
from helpers import USER_ID, get_review_content
from knobs import ScoreKnob, ProgressKnob

def manga_review(anilist_manga_id):
    cache = current_app.cache

    try:
        media_list = get_media_list(anilist_manga_id, USER_ID)
        presenter = MediaListPresenter(media_list)
        score_knob = ScoreKnob(presenter.score, 200, presenter.media.color)

        progress_knob = ProgressKnob(presenter.to_percent(cache=False), 200, presenter.media.color)

        review_content = get_review_content(presenter)

        cache.set(f"{presenter.media.id}.review", review_content)

        completed_at_or_today = presenter.completed_at if presenter.completed_at else date.today()
        time_range = completed_at_or_today - presenter.started_at if presenter.started_at else None

        return render_template("manga_review.html", presenter=presenter, score_knob=score_knob, progress_knob=progress_knob, review_content=review_content, time_range=time_range, completed_at_or_today=completed_at_or_today)
    except APIException as exception:
        return "Not found", exception.status_code
