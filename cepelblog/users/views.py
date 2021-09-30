"""
cepelblog/users/views.py
"""

from logging import log
from operator import methodcaller
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from flask_login.utils import login_required
from cepelblog import db
from cepelblog.models import User, BlogPost
from cepelblog.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

# -----------------------------------------------------------------------------
# REGISTER USER VIEW
# -----------------------------------------------------------------------------

# @users.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()

#     if form.validate_on_submit():
#         user = User(email=form.email.data,
#                     username = form.username.data,
#                     password = form.password.data
#         )

#         db.session.add(user)
#         db.session.commit()
#         flash('Thanks for registration!')

#         return redirect(url_for('users.login'))
    
#     return render_template('register.html', form=form)

# -----------------------------------------------------------------------------
# LOG IN USER VIEW
# -----------------------------------------------------------------------------

@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log In Success!')

            next = request.args.get('next') # grab the information user wants to access

            if next == None or not next[0] == '/':
                next = url_for('core.index') 
            
            return redirect(next) 

    return render_template('login.html', form=form)


# -----------------------------------------------------------------------------
# LOG OUT VIEW
# -----------------------------------------------------------------------------

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# -----------------------------------------------------------------------------
# USER BLOGS VIEW
# -----------------------------------------------------------------------------

@users.route('/posts/<username>/')
def posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
