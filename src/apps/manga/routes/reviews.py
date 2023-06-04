import math
from flask import render_template

from api.anilist import get_media_list
from api.exceptions import APIException
from api.presenters import MediaListPresenter
from knobs import ScoreKnob, ProgressKnob
from .latest_chapter import latest_chapter

def manga_review(anilist_manga_id):
    try:
        media_list = get_media_list(anilist_manga_id, 5613718)
        presenter = MediaListPresenter(media_list)
        score_knob = ScoreKnob(presenter.score, 200, presenter.media.color)

        if presenter.media.chapters:
            maximum = presenter.media.chapters
        else:
            chapters, _ = latest_chapter(presenter.media)
            maximum = chapters if presenter.progress < chapters else presenter.progress
        if maximum > 0:
            percent = math.floor((presenter.progress / maximum) * 100)
        else:
            percent = 0
        progress_knob = ProgressKnob(percent, 200, presenter.media.color)

        if presenter.is_current() and presenter.media.is_finished():
            # Don't bother getting reviews for a currently reading finished manga
            review_content = "I'm currently reading this manga, so I haven't written a review yet."
        else:
            # TODO: Get review
            review = None
            review_content = "I haven't written a review for this manga yet." if not review else review.content

        return render_template("manga_review.html", presenter=presenter, score_knob=score_knob, progress_knob=progress_knob, review_content=review_content)
    except APIException as exception:
        return "Not found", exception.status_code
