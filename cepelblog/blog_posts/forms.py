"""
cepelblog/blog_posts/forms.py
"""

from cepelblog.models import Tag
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from cepelblog import db

def get_tags():
    return db.session.query(Tag).all()

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = CKEditorField('Blog Content', validators=[DataRequired()])
    tag = QuerySelectMultipleField('Tag', validators=[DataRequired()], query_factory=get_tags)
    picture = FileField('Update Blog Banner', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')