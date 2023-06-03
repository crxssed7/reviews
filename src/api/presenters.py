import math

class KnobPresenter:
    def __init__(self, percent, radius, color):
        self.radius = radius
        self.percent = percent
        self.color = color
        self.circumfrence = self.radius * 2 * math.pi
        if self.percent:
            self.percent_as_circle = (100 - self.percent) / 100 * self.circumfrence
            self.text = self.get_text()
        else:
            self.percent_as_circle = self.circumfrence
            self.text = "N/A"
        self.dimensions = self.radius + 10
        self.viewport = self.dimensions * 2

    def to_html(self):
        return """
        <svg width="{dimensions}" height="{dimensions}" viewBox="0 0 {viewport} {viewport}">
            <circle
                stroke-width="10"
                stroke="#080808"
                fill="transparent"
                r="{radius}"
                cx="{dimensions}"
                cy="{dimensions}"
            />
            <circle
                stroke-width="20"
                stroke-dasharray="{circumfrence}"
                stroke-dashoffset="{percent_as_circle}"
                stroke-linecap="square"
                stroke="{color}"
                fill="transparent"
                r="{radius}"
                cx="{dimensions}"
                cy="{dimensions}"
                transform="rotate(-90 {dimensions} {dimensions})"
            />
            <text x="50%" y="50%" fill="{color}" style="font-family: 'Montserrat'; font-size: 75px; font-weight: bold;" dominant-baseline="middle" text-anchor="middle">{text}</text>
        </svg>
        """.format(dimensions=self.dimensions, viewport=self.viewport, radius=self.radius, circumfrence=self.circumfrence, percent_as_circle=self.percent_as_circle, color=self.color, text=self.text)

    def get_text(self):
        return ""

class ScorePresenter(KnobPresenter):
    def __init__(self, percent, radius, color):
        if percent:
            percent *= 10
        super(ScorePresenter, self).__init__(percent, radius, color)

    def get_text(self):
        return f"{int(self.percent / 10)} / 10"

class ProgressPresenter(KnobPresenter):
    def get_text(self):
        return f"{self.percent}%"

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
