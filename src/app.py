from flask import Flask
from apps.manga.views import manga

def create_app():
    app = Flask(__name__)

    app.register_blueprint(manga, url_prefix="/")

    return app

if __name__ == "__main__":
    create_app().run()
