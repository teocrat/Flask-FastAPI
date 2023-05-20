from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello!!!'


@app.route('/main/')
def main():
    context = {'title': 'Main'}
    return render_template('main.html', **context)


@app.route('/contacts/')
def contacts():
    context = {'title': 'Contacts'}
    return render_template('contacts.html', **context)


@app.route('/about/')
def about():
    context = {'title': 'About'}
    return render_template('about.html', **context)


if __name__ == '__main__':
    app.run()
