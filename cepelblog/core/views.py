"""
cepelblog/core/views.py
"""

from cepelblog.models import BlogPost, Tag
from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)

# -----------------------------------------------------------------------------
# INDEX VIEW
# -----------------------------------------------------------------------------

@core.route('/')
def index():
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).limit(4).all()
    tags = Tag.query.all()
    return render_template('index.html', blog_posts=blog_posts, tags=tags)

# -----------------------------------------------------------------------------
# BLOG VIEW
# -----------------------------------------------------------------------------

@core.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10, error_out=False)
    tags = Tag.query.all()
    return render_template('blog.html', blog_posts=blog_posts, tags=tags)

# -----------------------------------------------------------------------------
# ABOUT VIEW
# -----------------------------------------------------------------------------

@core.route('/about')
def about():
    return render_template('about.html')