from flask import render_template, redirect, Blueprint, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required

from myproject.extentions import db
from myproject.models import User, BlogPost
from myproject.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from myproject.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        print("form is valid")
        try:
            print("Creating user")
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            print(user)
            user.save_to_db()

            return redirect(url_for('users.login'))

        except Exception as e:
            return render_template('register.html', form=form, error_msg=str(e))

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User.query.filter_by(email=form.username.data).first()
            if user is None:
                return render_template('login.html', form=form, error_msg="Username/email not found")

        try:
            check_pass = user.check_password_hash(form.password.data)
            if check_pass:
                login_user(user)

                next_page = request.args.get('next')
                print(next_page)
                if next_page is None:
                    next_page = url_for('core.index')

                return redirect(next_page)
            else:
                return render_template('login.html', form=form, error_msg="Incorrect username or password")

        except Exception as e:
            return render_template('login.html', form=form, error_msg=str(e)), 500

    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        try:
            if form.picture.data:
                username = current_user.username
                current_user.profile_image = add_profile_pic(form.picture.data, username)

            current_user.username = form.username.data
            current_user.email = form.username.data
            db.session.commit()

            flash("User data updated")
            return redirect(url_for('users.account'))
        except Exception as e:
            return render_template('account.html', form=form, error_msg=str(e))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('user_blog_posts.html', user=user, blog_posts=blog_posts)
