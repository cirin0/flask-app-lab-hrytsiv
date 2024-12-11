from flask import flash, redirect, render_template, abort, url_for

from app.posts.models import Post, Tag
from app import db

from app.users.models import User

from .forms import PostForm
from . import post_bp


@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.posted.asc()).all()
    return render_template('posts.html', posts=posts)


@post_bp.route('/<int:id>')
def get_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)
    return render_template('detail-post.html', post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    # if 'username' not in session:
    # flash('Please login to add a post', 'danger')
    # return redirect(url_for('users.login'))
    authors = User.query.all()
    author_choices = [(author.id, author.username) for author in authors]
    form = PostForm()
    form.author.choices = author_choices
    if form.validate_on_submit():

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.posted.data,
            category=form.category.data,
            user_id=form.author.data
        )
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        new_post.tags.extend(selected_tags)

        db.session.add(new_post)
        db.session.commit()

        flash('Post added successfully', 'success')
        return redirect(url_for('.get_posts'))
    return render_template('add-post.html', form=form)


@post_bp.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    post = Post.query.get(id)

    if post is None:
        abort(404)

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('.get_posts'))


@post_bp.route('/edit_post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = db.get_or_404(Post, id)
    authors = User.query.all()
    author_choices = [(author.id, author.username) for author in authors]
    form = PostForm(obj=post)
    form.author.choices = author_choices
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.posted = form.posted.data
        post.category = form.category.data
        post.user_id = form.author.data
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = selected_tags

        db.session.commit()

        flash('Post updated successfully', 'success')
        return redirect(url_for('.get_posts'))

    return render_template('edit-post.html', form=form, post=post)
