import math
from flask import render_template, current_app

from api.anilist import get_media_list
from api.exceptions import APIException
from api.presenters import MediaListPresenter
from helpers import latest_chapter_by_anilist, USER_ID, get_review_content
from knobs import ScoreKnob, ProgressKnob

def manga_review(anilist_manga_id):
    cache = current_app.cache

    try:
        media_list = get_media_list(anilist_manga_id, USER_ID)
        presenter = MediaListPresenter(media_list)
        score_knob = ScoreKnob(presenter.score, 200, presenter.media.color)

        if presenter.media.chapters:
            maximum = presenter.media.chapters
        else:
            chapters, _ = latest_chapter_by_anilist(presenter.media)
            maximum = chapters if presenter.progress < chapters else presenter.progress
        if maximum > 0:
            percent = math.floor((presenter.progress / maximum) * 100)
        else:
            percent = 0
        progress_knob = ProgressKnob(percent, 200, presenter.media.color)

        review_content = get_review_content(presenter)

        cache.set(f"{presenter.media.id}.review", review_content)

        return render_template("manga_review.html", presenter=presenter, score_knob=score_knob, progress_knob=progress_knob, review_content=review_content)
    except APIException as exception:
        return "Not found", exception.status_code
