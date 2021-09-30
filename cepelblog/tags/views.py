"""
cepelblog/tags/views.py
"""

from cepelblog.tags.forms import TagForm
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from cepelblog import db
from cepelblog.models import Tag

tags = Blueprint('tags', __name__)

# -----------------------------------------------------------------------------
# CREATE TAG VIEW
# -----------------------------------------------------------------------------

@tags.route('/tag/create_tag', methods=['GET', 'POST'])
@login_required
def create():
    form = TagForm()

    if form.validate_on_submit():
        tag = Tag(name=form.name.data)

        db.session.add(tag)
        db.session.commit()
        flash('Tag Created!')
        return redirect(url_for('tags.list'))
    
    return render_template('create_tag.html', form=form)

# -----------------------------------------------------------------------------
# LIST TAGS VIEW
# -----------------------------------------------------------------------------

@tags.route('/tag')
def list():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

# -----------------------------------------------------------------------------
# UPDATE TAG VIEW
# -----------------------------------------------------------------------------

@tags.route('/tag/update/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def update(category_id):
    tag = Tag.query.get_or_404(category_id)
    
    form = TagForm()

    if form.validate_on_submit():
        tag.name = form.name.data

        db.session.commit()
        flash('Tag Updated!')
        return redirect(url_for('tags.tags', category_id=category_id))

    elif request.method == 'GET':
        form.name.data = tag.name
    
    return render_template('create_tag.html', form=form)

# -----------------------------------------------------------------------------
# DELETE TAG VIEW
# -----------------------------------------------------------------------------

@tags.route('/<int:tag_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    db.session.delete(tag)
    db.session.commit()
    flash('Tag Deleted!')
    return redirect(url_for('tags.list'))