"""
cepelblog/__init__.py
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, event
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret"
ckeditor = CKEditor(app)
Bootstrap(app)

# -----------------------------------------------------------------------------
# DATABASE SETUP
# -----------------------------------------------------------------------------

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

# -----------------------------------------------------------------------------
# LOGIN CONFIGURATIONS
# -----------------------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from cepelblog.core.views import core
from cepelblog.users.views import users
from cepelblog.blog_posts.views import blog_posts
from cepelblog.tags.views import tags

# -----------------------------------------------------------------------------
# REGISTER BLUEPRINTS
# -----------------------------------------------------------------------------

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(tags)