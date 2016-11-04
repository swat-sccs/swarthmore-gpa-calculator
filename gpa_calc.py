import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
                  render_template, flash
from helpers import parse_grades, calculate_gpa

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        raw_grades = request.form['grades']
        try:
            grades = parse_grades(raw_grades)
            gpa = calculate_gpa(grades)
        except KeyError:
            return render_template('home.html', notice="Invalid grades")

        return render_template('gpa.html', gpa=gpa)
    else:
        return render_template('home.html')



