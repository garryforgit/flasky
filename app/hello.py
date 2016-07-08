# coding:utf-8

from flask import Flask, render_template, session, \
    redirect, url_for, flash
from flask_script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime  # print the local time
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField \
    # get the text data and commit button data .
from wtforms.validators import Required \
    # Required validata the data is not null

app = Flask(__name__)
app.config['SECRET_KEY'] = 'do not you trust me '
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


# view function
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("Things like you have changed your name!")
        session['name'] = form.name.data
        return redirect(url_for('index'))  # url_for must get 1
        # arguments, it is view function,here is index()
    return render_template('index.html', \
                           form=form, name=session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


class NameForm(Form):
    # name 是一个文本字段 变量,具体表示为type='text'的<input>元素
    name = StringField('What is your name?', validators=[Required()])
    # SubmitField is > type="submit"的,<input>元素
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
