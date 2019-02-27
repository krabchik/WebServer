from flask_wtf import FlaskForm
from flask import render_template, Flask, redirect, request
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return render_template('loginform.html')
    else:
        print(request.form.get('email'))
        print(request.form.get('password'))
        print(request.form.get('class'))
        print(request.form.get('about'))
        print(request.form.get('accept'))
        print(request.form.get('sex'))

        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
