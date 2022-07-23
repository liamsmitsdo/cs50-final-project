from flask import Blueprint, jsonify, render_template, request, flash
from flask_login import login_required, current_user
from .models import Post
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():

    if request.method == 'POST':
        post = request.form.get('post')

        if len(post) < 1:
            flash('Note is too short', category='failure')
        else:
            new_post = Post(desc=post, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Note added', category='success')

    return render_template('index.html', user=current_user)


@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Post.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})