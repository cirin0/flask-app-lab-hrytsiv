from flask import render_template, request, redirect, url_for, abort
from . import app


@app.route('/')
def main():
    return render_template('hello.html')


@app.route('/homepage')
def home():
    """View foe the Home page of your website"""
    agent = request.user_agent

    return render_template('home.html', agent=agent)


@app.route('/resume')
def resume():
    return render_template('resume.html', title='Моє резюме')
