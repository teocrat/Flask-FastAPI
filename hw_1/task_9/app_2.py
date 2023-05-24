from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello!!!'


@app.route('/main/')
def main():
    context = {'title': 'Main'}
    return render_template('main.html', **context)


@app.route('/cloth/')
def cloth():
    context = {'title': 'Cloth'}
    return render_template('cloth.html', **context)


@app.route('/shoes/')
def shoes():
    context = {'title': 'Shoes'}
    return render_template('shoes.html', **context)


@app.route('/jacket/')
def jacket():
    context = {'title': 'Jacket'}
    return render_template('jacket.html', **context)


if __name__ == '__main__':
    app.run()
