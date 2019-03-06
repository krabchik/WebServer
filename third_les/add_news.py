from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask import redirect, render_template, Flask, session
from database import DB, UsersModel, NewsModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

DB_NAME = 'news.db'

db = DB(DB_NAME)
user_model = UsersModel(db.get_connection())
user_model.insert('human', 'password')
news_model = NewsModel(db.get_connection())
news_model.insert('novost', 'kolobok povesilsa', 0)


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    return redirect('/main')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect('/main')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/main')
def main():
    news = news_model.get_all(session['user_id'])
    return render_template('main.html', title='Главная', username=session['username'],
                               news=news)


@app.route('/add_news')
def add_news():
    form = AddNewsForm()
    if form.validate_on_submit():
        return redirect('/main')
    return render_template('add_news.html', title='Добавление новости', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
