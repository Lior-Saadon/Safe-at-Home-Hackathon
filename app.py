# importing general extensions of flask here
from flask import Flask, session, render_template, request, flash, url_for, redirect
import flask
from flask_cors import CORS
import pandas as pd
import app_functions
import os

# The code for setting up a user session in flask and securing it with a secret_key is already installed below.
# You can jump directly to building your functions, and collecting HTML inputs for processing.

app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = app_functions.random_id(50)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        database = pd.read_csv('database.csv')
        session['email'] = request.form["email"]
        session['password'] = request.form["password"]

        if session['email'] in list(database['emails']):
            index = list(database['emails']).index(session['email'])

            if session['password'] == list(database['passwords'])[index]:
                session['name'] = database['name'][index]
                session['bmi'] = str(database['bmi'][index])
                return redirect(url_for('health'))

            else:
                flash('Incorrect username or password', 'error')
        else:
            flash('Incorrect username or password', 'error')

    return render_template('login.html')

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template('about.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        bmi = request.form['bmi']
        email = request.form["email"]
        password = request.form["password"]
        password2 = request.form["password2"]

        if password != password2:
            flash('The passwords dont match. Please try again.', 'error')
        else:
            database = pd.read_csv('database.csv')

            if email in list(database['emails']):
                flash('An Account with the same email exists.', 'error')
            else:
                database.loc[len(database)] = [email, password, name, bmi]
                database.to_csv('database.csv', index=False)
                flash('Your Account has been successfuly created. You may log in now.', 'success')
                return(redirect(url_for('login')))

    return render_template('sign_up.html')

@app.route("/health", methods=["GET", "POST"])
def health():
    if 'name' not in session:
        flash('You are not logged in. Please log in first.', 'error')
        return redirect(url_for('login'))

    return render_template('health.html',
                            bmi = session['bmi'],
                            name = session['name'],
                            current_status = 'caution',
                            heart_rate_status = 'caution')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.errorhandler(404)
def page_not_found(e):
    # the flash utlity flashes a message that can be shown on the main HTML page
    flash('The URL you entered does not exist. You have been redirected to the home page')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
