from flask import Blueprint
from .routes.index import manga_index, status
from .routes.reviews import manga_review, load_activities
from .routes.latest_chapter import manga_lastest_chapter

manga = Blueprint('manga', __name__)

manga.add_url_rule('/', 'manga_index', manga_index)
manga.add_url_rule('/<string:status>', 'manga_status', status)
manga.add_url_rule('/manga/<int:anilist_manga_id>', 'manga_review', manga_review)
manga.add_url_rule('/manga/<int:anilist_manga_id>/activities/<int:page>', 'load_activities', load_activities)
manga.add_url_rule('/chapter/<int:anilist_manga_id>', 'manga_latest_chapter', manga_lastest_chapter)
