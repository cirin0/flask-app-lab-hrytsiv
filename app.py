from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def main():
    return '<h1>Hello, World!</h1>', 200


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent

    return f'This is your Home page - {agent}'


@app.route('/hi/<string:name>')
def greeting(name):
    name = name.upper()
    age = request.args.get('age', 0, int)
    year = 2024 - age
    return f'Welcome, {name} - {year}!'


if __name__ == '__main__':
    app.run(debug=True)
