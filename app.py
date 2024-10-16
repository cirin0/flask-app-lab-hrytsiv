from flask import Flask
app = Flask(__name__)


@app.route('/')
def main():
    return '<h1>Hello, World!</h1>', 200


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""

    return 'This is your Home page'


if __name__ == '__main__':
    app.run(debug=True)
