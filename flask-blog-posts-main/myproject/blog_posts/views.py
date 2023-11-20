from flask import render_template, redirect, Blueprint, abort, request, url_for
from flask_login import login_required, current_user

from myproject.extentions import db
from myproject.models import BlogPost
from .forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        try:
            blog_post = BlogPost(title=form.title.data, text=form.text.data,
                                 user_id=current_user.id)

            blog_post.save_to_db()
            return redirect(url_for('core.index'))
        except Exception as e:
            return render_template('create_posts.html', form=form, error_msg=str(e))
    return render_template('create_posts.html', form=form)


@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_posts.html', title=blog_post.title, post=blog_post, date=blog_post.date)


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.text = form.text.data
        blog_post.title = form.title.data
        try:
            db.session.commit()
        except Exception as e:
            return render_template('create_posts.html', form=form, error_msg=str(e)), 500

    elif request.method == 'GET':
        form.text.data = blog_post.text
        form.title.data = blog_post.title

    return render_template('create_posts.html', form=form)


@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    try:
        blog_post.delete_post()
    except:
        return "<h3 style='color:red'>Internal Server Error</h3>", 500

    return redirect(url_for('core.index'))
