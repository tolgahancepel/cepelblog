"""
cepelblog/blog_posts/views.py
"""

import os
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from cepelblog import db
from cepelblog.models import BlogPost, Tag, tag_post_table
from cepelblog.blog_posts.forms import BlogPostForm
from cepelblog.blog_posts.picture_handler import add_blog_banner

blog_posts = Blueprint('blog_posts', __name__)

# -----------------------------------------------------------------------------
# CREATE BLOGPOST VIEW
# -----------------------------------------------------------------------------

@blog_posts.route('/blog/create', methods=['GET', 'POST'])
@login_required
def create_post():
    
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id,
                             tags=form.tag.data
        )

        if form.picture.data:
            pic = add_blog_banner(form.picture.data)
            blog_post.banner_image = pic
        
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created!')
        return redirect(url_for('core.index'))
    
    return render_template('create_post.html', form=form)

# -----------------------------------------------------------------------------
# UPDATE BLOGPOST VIEW
# -----------------------------------------------------------------------------

@blog_posts.route('/blog/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)
    
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        blog_post.tags = form.tag.data

        if form.picture.data:
            if(blog_post.banner_image != 'default_banner.png'):
                basedir = os.path.abspath(os.path.dirname(__file__))
                img_dir = os.path.join(basedir, '..', 'static', 'blog_banners', blog_post.banner_image)
                os.remove(img_dir)

            pic = add_blog_banner(form.picture.data)
            blog_post.banner_image = pic

        db.session.commit()
        flash('Blog Post Updated!')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    
    banner_img = url_for('static', filename='blog_banners/'+blog_post.banner_image)

    print("#############################")
    print(banner_img)
    return render_template('create_post.html', banner_img=banner_img,
                           blog_post=blog_post, title='Updating', form=form)

# -----------------------------------------------------------------------------
# DELETE BLOGPOST VIEW
# -----------------------------------------------------------------------------

@blog_posts.route('/blog/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)
    
    if(blog_post.banner_image != 'default_banner.png'):
        basedir = os.path.abspath(os.path.dirname(__file__))
        img_dir = os.path.join(basedir, '..', 'static', 'blog_banners', blog_post.banner_image)
        os.remove(img_dir)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted!')
    return redirect(url_for('core.index'))

# -----------------------------------------------------------------------------
# SINGLE BLOGPOST VIEW
# -----------------------------------------------------------------------------

@blog_posts.route('/blog/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                           date=blog_post.date, post=blog_post
    )

# -----------------------------------------------------------------------------
# TAG BLOGPOSTS VIEW
# -----------------------------------------------------------------------------

@blog_posts.route('/blog/<tag_name>')
def tag(tag_name):
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.join(tag_post_table).join(Tag)\
    .filter((tag_post_table.c.post_id == BlogPost.id) & (tag_post_table.c.tag_id == Tag.id) & (Tag.name == tag_name))\
    .order_by(BlogPost.date.desc())\
    .paginate(page=page, per_page=10, error_out=False)
    return render_template('tag_posts.html', blog_posts=blog_posts, tag_name=tag_name)