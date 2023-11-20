from flask import Flask

from .commands import create_tables
from .extentions import db, login_manager


# from flask_migrate import Migrate


def create_app(config_file="settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    # Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    from myproject.core.views import core
    from myproject.users.views import users
    from myproject.blog_posts.views import blog_posts
    from myproject.error_pages.handlers import error_pages

    app.register_blueprint(core)
    app.register_blueprint(users)
    app.register_blueprint(error_pages)
    app.register_blueprint(blog_posts)

    app.cli.add_command(create_tables)

    return app
