from flask import Flask
from flask_caching import Cache

from apps.manga.views import manga

from helpers import USER_NAME, USER_AVATAR, DEBUG

def create_app():
    app = Flask(__name__)

    config = {
        "DEBUG": DEBUG,
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 259200
    }

    app.config.from_mapping(config)
    app.jinja_env.globals.update(username=USER_NAME)
    app.jinja_env.globals.update(avatar=USER_AVATAR)
    app.jinja_env.globals.update(round=round)
    app.register_blueprint(manga, url_prefix="/")

    cache = Cache(app)
    app.cache = cache

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
