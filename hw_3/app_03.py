from flask import Flask, render_template, request
from lesson_3.hw_3.models_03 import db, User
from lesson_3.hw_3.regisrer_form import RegisterForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reg_users.db'
app.config['SECRET_KEY'] = b'269bdff6dc28c8913c19876bd7b96c5da60089884e3db4f2638d452d0a383295'
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        p = generate_password_hash(password)
        user = User(first_name=first_name, last_name=last_name, email=email, password=p)
        db.session.add(user)
        db.session.commit()
        return 'Registration successful'
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run()
