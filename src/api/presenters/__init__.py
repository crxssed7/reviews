import datetime
import math

from bs4 import BeautifulSoup
from flask import url_for

from helpers import get_cached_latest_chapter, latest_chapter_by_anilist, AL_STATUSES

DEMOGRAPHS = [
    "Shounen",
    "Seinen",
    "Shoujo",
    "Josei"
]

class BasePresenter:
    def __init__(self, data):
        self.data = data

class MediaPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaPresenter, self).__init__(data)
        self.id = self.data["id"]
        self.description = self._fix_description(self.data["description"])
        self.romaji = self.data["title"]["romaji"]
        self.english_title = self.data["title"]["english"]
        self.banner_image = self.data["bannerImage"] or url_for("static", filename="img/default_banner.png")
        self.cover_image = self.data["coverImage"]["large"]
        self.color = self.data["coverImage"]["color"] or "#808080"
        self.chapters = self.data["chapters"]
        self.volumes = self.data["volumes"]
        self.status = self.data["status"]
        self.start_date = self.data["startDate"]
        self.tags = self.data["tags"]
        self.genres = self.data["genres"]

    def is_finished(self):
        return self.status == "FINISHED"

    def demographs(self):
        return list(filter(lambda x: x["name"] in DEMOGRAPHS, self.tags))

    def _fix_description(self, description):
        if description is None:
            return description
        soup = BeautifulSoup(description, "html.parser")
        return str(soup)

class MediaListPresenter(BasePresenter):
    def __init__(self, data, activities):
        super(MediaListPresenter, self).__init__(data)
        self.media = MediaPresenter(self.data["media"])
        self.custom_lists = self.data.get("customLists")
        if self.custom_lists:
            self.collecting = self.custom_lists.get("Collecting", False)
            self.favourite = self.custom_lists.get("Favourites", False)
        else:
            self.collecting = False
            self.favourite = False
        self.notes = self.data["notes"]
        self.score = self.data["score"] if self.data["score"] > 0 else None
        self.status = self.data["status"]
        self.progress = self.data["progress"]
        self.priority = self.data["priority"]
        self.completed_at = self.generate_date(self.data["completedAt"])
        self.started_at = self.generate_date(self.data["startedAt"])
        self.created_at = datetime.datetime.fromtimestamp(self.data["createdAt"])
        self.index_status = AL_STATUSES.get(self.status)
        self.number_of_activities = 0
        if activities:
            self.activities = []
            for activity in activities["activities"]:
                self.activities.append(ActivityPresenter(activity))
            self.number_of_activities = len(self.activities)

    def is_current(self):
        return self.status == "CURRENT"

    def is_completed(self):
        return self.status == "COMPLETED"

    def is_dropped(self):
        return self.status == "PAUSED" or self.status == "DROPPED"

    def generate_date(self, date_dict):
        if not date_dict:
            return None

        year = date_dict["year"]
        month = date_dict["month"]
        day = date_dict["day"]

        if not year or not month or not day:
            return None

        return datetime.date(year, month, day)

    def get_maximum(self, cache=True):
        if self.media.chapters:
            return self.media.chapters

        if cache:
            cached = get_cached_latest_chapter(self.media)
            if cached:
                chapters = cached.get("chapters", 0)
                return chapters if self.progress < chapters else self.progress
            return self.progress

        chapters, _ = latest_chapter_by_anilist(self.media)
        return chapters if self.progress < chapters else self.progress

    def to_percent(self, cache=True):
        if self.is_completed():
            return 100

        maximum = self.get_maximum(cache=cache)

        if maximum > 0:
            return math.floor((self.progress / maximum) * 100)
        return 0

    def score_icon(self):
        if self.score:
            if self.score == 10:
                return "<i class='p-2 fa-brands fa-web-awesome' title='10 / 10'></i>"
            return f"<i class='p-2 fa-solid fa-{self.score}' title='{self.score} / 10'></i>"
        return ""

    def reasonable_time(self):
        if self.completed_at:
            return f"Completed: {self.completed_at.strftime("%B %d, %Y")}"
        if self.started_at:
            return f"Started: {self.started_at.strftime("%B %d, %Y")}"
        return f"Listed: {self.created_at.strftime("%B %d, %Y")}"

class MediaListGroupPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaListGroupPresenter, self).__init__(data)
        self.name = self.data["name"]
        self.custom_list = self.data["isCustomList"]
        self.status = self.data["status"]
        self.entries = []
        for entry in self.data["entries"]:
            self.entries.append(MediaListPresenter(entry, None))

    def sort_by(self, attr, reverse = False):
        ordered = self.entries
        ordered = list(filter(lambda entry : getattr(entry, attr) != None, ordered))
        ordered.sort(key=lambda x: getattr(x, attr), reverse=reverse)
        self.entries = ordered
        return self

class MediaListCollectionPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaListCollectionPresenter, self).__init__(data)
        self.lists = []
        for entry in self.data["lists"]:
            self.lists.append(MediaListGroupPresenter(entry))

    def get_status(self, status):
        status_list = list(filter(lambda list_data : list_data.status == status, self.lists))
        if len(status_list) > 0:
            return status_list[0]
        return MediaListGroupPresenter({"name": "", "isCustomList": False, "status": status, "entries": []})

class ActivityPresenter(BasePresenter):
    def __init__(self, data):
        super(ActivityPresenter, self).__init__(data)
        self.created_at = datetime.datetime.utcfromtimestamp(self.data["createdAt"])
        self.status = self.data["status"]
        self.progress = self.data["progress"]
        self.colour = self.get_colour()

    def get_colour(self):
        colours = {
            "plans to read": "#FFD966",
            "read chapter": "#90ee90",
            "completed": "#65b2ff",
            "paused reading": "#ff6961",
            "dropped": "#ff6961"
        }
        return colours.get(self.status, "white")
