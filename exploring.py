from flask import Blueprint, request, flash, redirect, url_for, jsonify, render_template
from flask_login import current_user
from responses import *
import requests

# Defining blueprint
ex_path = Blueprint('ex_path', __name__)


# Displaying web page only
@ex_path.route('/force', methods=['GET'])
def show_force():
    if current_user.is_authenticated:  # Check for valid user
        return render_template('force.html')
    else:
        return render_template('login.html', response=error_401), 401


# If user requests information
@ex_path.route('/force', methods=['POST'])
def force_post():
    name = request.form.get('name').lower()  # Getting input and defining url
    url = 'https://data.police.uk/api/forces/{}'.format(name)
    # Make request to API and display response if ok
    try:
        resp = requests.get(url)
        if resp.ok:
            return jsonify(resp.json())
        else:
            error = str(resp.status_code) + " " + resp.reason
            flash(error)
    except Exception:
        error = str(resp.status_code) + " " + resp.reason
        flash(error)
    return redirect(url_for('ex_path.show_force'))


# Display Crime API page
@ex_path.route('/crime', methods=['GET'])
def show_crime():
    if current_user.is_authenticated:  # Check for valid user
        return render_template('crime.html')
    else:
        return render_template('login.html', response=error_401), 401


# Requesting for Crime API
@ex_path.route('/crime', methods=['POST'])
def crime_post():
    # Getting input from form and validating input
    crime_url_template = 'https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={date}'
    lat = request.form.get('lat')  # 51.52369
    lng = request.form.get('lng')  # -0.0395857
    date = request.form.get('date')  # 2018-11
    categorical = request.form.get('cats')
    if not all([lat, lng, date]):
        flash('All fields mandatory')
        return redirect(url_for('ex_path.show_crime'))
    else:  # Make request to API and display response if ok
        crime_url = crime_url_template.format(lat=lat, lng=lng, date=date)
        try:
            resp = requests.get(crime_url)
            if categorical:
                return categorical_data(date, resp)
            if resp.ok:
                return jsonify(resp.json())
            else:
                print(resp.reason)
        except Exception:
            error = str(resp.status_code) + " " + resp.reason
            flash(error)
    return


# Display Neighbourhood page
@ex_path.route('/neigh')
def show_neigh():
    if current_user.is_authenticated:  # Check for valid user
        return render_template('neigh.html')
    else:
        return render_template('login.html', response=error_401), 401


# Request Neighbourhood API
@ex_path.route('/neigh', methods=['POST'])
def neigh_post():
    name = request.form.get('name').lower()
    url = 'https://data.police.uk/api/{}/neighbourhoods'.format(name)
    try:
        resp = requests.get(url)
        if resp.ok:
            return jsonify(resp.json())
        else:
            error = str(resp.status_code) + " " + resp.reason
            flash(error)
    except Exception:
        error = str(resp.status_code) + " " + resp.reason
        flash(error)
    return redirect(url_for('ex_path.show_neigh'))


# If user requests for categorical count
def categorical_data(date, resp):
    categories_url_template = 'https://data.police.uk/api/crime-categories?date={date}'
    if resp.ok:
        crimes = resp.json()
    else:
        print(resp.reason)

    categories_url = categories_url_template.format(date = date)
    resp = requests.get(categories_url)
    if resp.ok:
        cat_json = resp.json()
    else:
        print(resp.reason)

    cats = {cat["url"]: cat["name"] for cat in cat_json}

    stats = dict.fromkeys(cats.keys(), 0)
    stats.pop("all-crime")

    for crime in crimes:
        stats[crime["category"]] += 1

    return jsonify(stats)
