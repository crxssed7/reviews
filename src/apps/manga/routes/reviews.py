from datetime import date
from flask import render_template, current_app, jsonify

from api.anilist import get_media_list
from api.exceptions import APIException
from api.presenters import MediaListPresenter, ActivityPresenter
from helpers import USER_ID, get_review_content, get_and_cache_activities
from knobs import ScoreKnob, ProgressKnob

def manga_review(anilist_manga_id):
    cache = current_app.cache

    try:
        media_list = get_media_list(anilist_manga_id, USER_ID)
        activities = get_and_cache_activities(anilist_manga_id)

        presenter = MediaListPresenter(media_list, activities)
        score_knob = ScoreKnob(presenter.score, 200, presenter.media.color)

        progress_knob = ProgressKnob(presenter.to_percent(cache=False), 200, presenter.media.color)

        review_content = get_review_content(presenter)

        completed_at_or_today = presenter.completed_at if presenter.completed_at else date.today()
        time_range = completed_at_or_today - presenter.started_at if presenter.started_at else None

        return render_template("manga_review.html", presenter=presenter, score_knob=score_knob, progress_knob=progress_knob, review_content=review_content, time_range=time_range, completed_at_or_today=completed_at_or_today)
    except APIException as exception:
        return "Not found", exception.status_code

def load_activities(anilist_manga_id, page):
    cache = current_app.cache

    try:
        activities = get_and_cache_activities(anilist_manga_id, page=page)

        if not activities:
            return jsonify({"activities": []})

        activity_response = []
        cache.set(f"{anilist_manga_id}.activities.{page}", activities)
        for activity in activities["activities"]:
            presenter = ActivityPresenter(activity)
            activity_response.append({
                "createdAt": presenter.created_at.strftime("%B %d %Y, %H:%M"),
                "progress": presenter.progress,
                "status": presenter.status,
                "colour": presenter.colour
            })
        return jsonify({"activities": activity_response})

    except APIException as exception:
        return "Not found", exception.status_code
