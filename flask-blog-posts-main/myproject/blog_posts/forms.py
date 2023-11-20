from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text')
    submit = SubmitField('Post')