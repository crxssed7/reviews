from datetime import date
import datetime
from flask import render_template, current_app, jsonify

from api.anilist import get_media_list
from api.exceptions import APIException
from api.presenters import MediaListPresenter, ActivityPresenter
from helpers import USER_ID, get_review_content, get_and_cache_activities, recursively_retrieve_activities
from knobs import ScoreKnob, ProgressKnob

def manga_review(anilist_manga_id):
    try:
        media_list = get_media_list(anilist_manga_id, USER_ID)
        # TODO: Extract this, make the frontend request it
        activities = recursively_retrieve_activities(anilist_manga_id)

        presenter = MediaListPresenter(media_list, activities)
        score_knob = ScoreKnob(presenter.score, 200, presenter.media.color)

        progress_knob = ProgressKnob(presenter.to_percent(cache=False), 200, presenter.media.color)

        review_content = get_review_content(presenter)

        print(presenter.durations)

        return render_template("manga_review.html", presenter=presenter, score_knob=score_knob, progress_knob=progress_knob, review_content=review_content)
    except APIException as exception:
        return "Not found", exception.status_code

def load_activities(anilist_manga_id, page):
    cache = current_app.cache

    try:
        activities = get_and_cache_activities(anilist_manga_id, page=page)

        if not activities:
            return jsonify({"activities": []})

        activity_response = []
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
