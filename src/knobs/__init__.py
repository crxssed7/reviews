import math

class BaseKnob:
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
                transform="rotate(-90 {dimensions} {dimensions})">
                    <animate
                        attributeName="stroke-dashoffset"
                        values="{circumfrence};{percent_as_circle}"
                        dur="0.5s"
                        repeatCount="1"
                    />
            </circle>
            <text x="50%" y="50%" fill="{color}" style="font-family: 'Montserrat'; font-size: 70px; font-weight: bold;" dominant-baseline="middle" text-anchor="middle">{text}</text>
        </svg>
        """.format(dimensions=self.dimensions, viewport=self.viewport, radius=self.radius, circumfrence=self.circumfrence, percent_as_circle=self.percent_as_circle, color=self.color, text=self.text)

    def get_text(self):
        return ""

class ScoreKnob(BaseKnob):
    SCORE_TEXT = {
        1: "Horrific",
        2: "Bad",
        3: "Bad",
        4: "Bad",
        5: "Meh",
        6: "Meh",
        7: "Good",
        8: "Good",
        9: "Amazing",
        10: "Terrific"
    }

    def __init__(self, percent, radius, color):
        if percent:
            percent *= 10
        super(ScoreKnob, self).__init__(percent, radius, color)

    def get_text(self):
        return self.SCORE_TEXT[self.percent / 10]

class ProgressKnob(BaseKnob):
    def get_text(self):
        return f"{self.percent}%"
