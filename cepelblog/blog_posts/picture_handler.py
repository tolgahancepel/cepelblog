"""
cepelblog/blog_posts/picture_handler.py
"""

import os
from PIL import Image
from flask import current_app
import uuid

def add_blog_banner(pic_upload):
    
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = uuid.uuid4().hex + '.' + ext_type
    filepath = os.path.join(current_app.root_path, 'static/blog_banners', storage_filename)

    output_size = (1000, 500)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename