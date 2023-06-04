from flask import Flask
from flask_caching import Cache
from apps.manga.views import manga

def create_app():
    app = Flask(__name__)

    config = {
        "DEBUG": True,
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 120
    }

    app.config.from_mapping(config)
    app.register_blueprint(manga, url_prefix="/")

    cache = Cache(app)
    app.cache = cache

    return app

if __name__ == "__main__":
    create_app().run()
