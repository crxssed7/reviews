import datetime
from flask import url_for

class BasePresenter:
    def __init__(self, data):
        self.data = data

class MediaPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaPresenter, self).__init__(data)
        self.id = self.data["id"]
        self.romaji = self.data["title"]["romaji"]
        self.english_title = self.data["title"]["english"]
        self.banner_image = self.data["bannerImage"] or url_for("static", filename="img/default_banner.png")
        self.cover_image = self.data["coverImage"]["large"]
        self.color = self.data["coverImage"]["color"] or "#202020"
        self.chapters = self.data["chapters"]
        self.status = self.data["status"]
        self.start_date = self.data["startDate"]

    def is_finished(self):
        return self.status == "FINISHED"

class MediaListPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaListPresenter, self).__init__(data)
        self.media = MediaPresenter(self.data["media"])
        self.collecting = self.data["customLists"]["Collecting"]
        self.favourite = self.data["customLists"]["Favourites"]
        self.notes = self.data["notes"]
        self.score = self.data["score"] if self.data["score"] > 0 else None
        self.status = self.data["status"]
        self.progress = self.data["progress"]
        self.priority = self.data["priority"]
        self.completed_at = self.generate_date(self.data["completedAt"])
        self.started_at = self.generate_date(self.data["startedAt"])

    def is_current(self):
        return self.status == "CURRENT"

    def generate_date(self, date_dict):
        if not date_dict:
            return None

        year = date_dict["year"]
        month = date_dict["month"]
        day = date_dict["day"]

        if not year or not month or not day:
            return None

        return datetime.date(year, month, day)

    def to_html(self):
        collecting_icon = "<i class='m-2 fa-solid fa-bookmark'></i>" if self.collecting else ""
        favourite_icon = "<i class='m-2 fa-solid fa-heart'></i>" if self.favourite else ""
        score_icon = f"<i class='m-2 fa-solid fa-{self.score}'></i>" if self.score else ""
        return f"""
        <a href="/manga/{self.media.id}" title="{self.media.romaji}">
            <div class="relative p-2 rounded min-w-[150px] w-[150px] h-[225px] bg-no-repeat bg-cover bg-center" style="background-image: url('{self.media.cover_image}');">
                <div class="text-gray-100 absolute rounded inline-block right-2 bottom-2 backdrop-blur-lg" style="background-color: {self.media.color}80;">
                    {score_icon}
                    {favourite_icon}
                    {collecting_icon}
                </div>
            </div>
        </a>
        """

class MediaListGroupPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaListGroupPresenter, self).__init__(data)
        self.name = self.data["name"]
        self.custom_list = self.data["isCustomList"]
        self.status = self.data["status"]
        self.entries = []
        for entry in self.data["entries"]:
            self.entries.append(MediaListPresenter(entry))

    def sort_by(self, attr, reverse = False):
        self.entries.sort(key=lambda x: getattr(x, attr), reverse=reverse)
        return self

class MediaListCollectionPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaListCollectionPresenter, self).__init__(data)
        self.lists = []
        for entry in self.data["lists"]:
            self.lists.append(MediaListGroupPresenter(entry))

    def get_status(self, status):
        status_list = filter(lambda list_data : list_data.status == status, self.lists)
        return list(status_list)[0]
