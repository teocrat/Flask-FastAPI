from markupsafe import escape

from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)
app.secret_key = b'269bdff6dc28c8913c19876bd7b96c5da60089884e3db4f2638d452d0a383295'


@app.route('/')
def index():
    if 'username' in session:
        context = {'title': 'hi', 'session': session["username"]}
        return render_template('hi.html', **context)
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        return redirect(url_for('index'))
    return render_template('username_form.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))


@app.route('/index/')
def main():
    context = {'title': 'main'}
    return render_template('index.html', **context)


@app.route('/contacts/')
def contacts():
    context = {'title': 'contacts'}
    return render_template('contacts.html', **context)


@app.route('/about/')
def about():
    context = {'title': 'about'}
    return render_template('about.html', **context)


@app.route('/square/', methods=['GET', 'POST'])
def square():
    context = {'title': 'square'}
    if request.method == 'POST':
        num = int(escape(request.form.get('num')))
        return f'Квадрат числа {num} = {num ** 2}'
    return render_template('square.html', **context)


if __name__ == '__main__':
    app.run()
