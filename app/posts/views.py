from flask import flash, redirect, render_template, abort, url_for, session

from .forms import PostForm
from . import post_bp
import json
import os

# posts = [
#     {"id": 1, 'title': 'My First Post',
#         'content': 'This is the content of my first post.', 'author': 'John Doe'},
#     {"id": 2, 'title': 'Another Day',
#         'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
#     {"id": 3, 'title': 'Flask and Jinja2',
#         'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
# ]

POSTS_FILE = 'posts.json'


def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, 'r') as file:
            return json.load(file)
    return []


def save_posts(posts):
    with open(POSTS_FILE, 'w') as file:
        json.dump(posts, file, indent=4)


posts = load_posts()


@post_bp.route('/')
def get_posts():
    posts = load_posts()
    return render_template('posts.html', posts=posts)


@post_bp.route('/<int:id>')
def get_post(id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        abort(404)
    return render_template('detail-post.html', post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'username' not in session:
        flash('Please login to add a post', 'danger')
        return redirect(url_for('users.login'))
    form = PostForm()
    if form.validate_on_submit():

        new_post = {
            'id': max([post['id'] for post in posts], default=0) + 1,
            'title': form.title.data,
            'content': form.content.data,
            'is_active': form.is_active.data,
            'publish_date': form.publish_date.data.strftime('%Y-%m-%d'),
            'category': form.category.data,
            'author': session.get('username', 'Anonymous')
        }

        posts.append(new_post)
        save_posts(posts)
        flash('Post added successfully', 'success')
        return redirect(url_for('.get_posts'))
    return render_template('add-post.html', form=form)
