from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
from gpa_calc import app
from gpa_calc.helpers import *

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/gpa', methods=['POST'])
def gpa():
    if request.method == 'POST':
        raw_grades = request.form['grades']
        grades = parse_grades(raw_grades)
        try:
            gpa = calculate_gpa(grades)
        except ZeroDivisionError: # No valid courses found in input
            flash("Invalid grade input")
            return redirect(url_for('index'))

        return render_template('gpa.html', gpa=gpa, courses=grades)
