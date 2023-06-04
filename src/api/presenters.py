class BasePresenter:
    def __init__(self, data):
        self.data = data

class MediaPresenter(BasePresenter):
    def __init__(self, data):
        super(MediaPresenter, self).__init__(data)
        self.romaji = self.data["title"]["romaji"]
        self.english_title = self.data["title"]["english"]
        # TODO: Set defaults
        self.banner_image = self.data["bannerImage"] or ""
        self.cover_image = self.data["coverImage"]["large"] or "https://tankobon.net/static/img/noposter.582688085a9c.png"
        self.color = self.data["coverImage"]["color"] or "#e5e7eb"
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

    def is_current(self):
        return self.status == "CURRENT"
