"""
views.py
Views for the Swat GPA calculator.
"""
from flask import Flask, request, redirect, url_for, render_template, flash
from gpa_calc import app
from gpa_calc.helpers import *

@app.route('/', methods=['GET'])
def index():
    """Homepage (with grades input field, etc.)"""
    return render_template('index.html')

@app.route('/gpa', methods=['GET', 'POST'])
def gpa():
    """GPA result page with GPA integral, list of courses"""
    if request.method == 'POST':
        grades = parse_grades(request.form['grades'])
        try:
            gpa = calculate_gpa(grades)
        except ZeroDivisionError: # No valid courses found in input
            flash("Invalid grade input") # Message appears on homepage
            return redirect(url_for('index'))

        gpa_integral = construct_integral(gpa)

        return render_template('gpa.html', gpa=gpa, gpa_integral=gpa_integral, \
                               courses=grades)
    else:
        return redirect(url_for('index'))
