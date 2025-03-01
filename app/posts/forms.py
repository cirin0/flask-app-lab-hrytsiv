from flask_wtf import FlaskForm
from wtforms import DateTimeLocalField, SelectMultipleField, StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from app.posts.models import Tag

CATEGORIES = [
    ('tech', 'Technology'),
    ('science', 'Science'),
    ('lifestyle', 'Lifestyle')
]


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', validators=[
                            DataRequired()], render_kw={'rows': 4, 'cols': 30})
    is_active = BooleanField('Active Post')
    posted = DateTimeLocalField('Publish Date', format='%Y-%m-%dT%H:%M')
    category = SelectField('Category', choices=CATEGORIES,
                           validators=[DataRequired()])
    author = SelectField('Author', coerce=int)
    tags = SelectMultipleField('Tags', coerce=int)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]

    submit = SubmitField('Add Post')
