from flask import render_template, request, Blueprint

from myproject.models import BlogPost

core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', blog_posts=blog_posts)

@core.route('/info')
def info():
    with open('/requirements_for_mysql.txt') as f:
        lines = f.readlines()
    return render_template('info.html', lines=lines)

