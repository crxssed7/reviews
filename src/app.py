import os

from flask import Flask
from flask_caching import Cache
from dotenv import load_dotenv

from apps.manga.views import manga

from helpers import USER_NAME, USER_AVATAR

load_dotenv()

def create_app():
    app = Flask(__name__)

    debug = os.getenv("REVIEWS_DEBUG", "False").lower() in ("true", "1", "t")

    config = {
        "DEBUG": debug,
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 259200
    }

    app.config.from_mapping(config)
    app.jinja_env.globals.update(username=USER_NAME)
    app.jinja_env.globals.update(avatar=USER_AVATAR)
    app.register_blueprint(manga, url_prefix="/")

    cache = Cache(app)
    app.cache = cache

    return app

if __name__ == "__main__":
    create_app().run()
