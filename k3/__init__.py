from flask import Flask

from .views import register_views
from .commandos import register_commands
from .config import Config, DevelopmentConfig
import logging

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config:Config=None) -> Flask:
    app = Flask(__name__)
    if config is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config)

    register_commands(app)
    register_views(app)

    return app