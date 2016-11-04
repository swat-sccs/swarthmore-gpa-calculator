from gpa_calc import app
from helpers import *

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/gpa', methods=['POST'])
def gpa():
    if request.method == 'POST':
        raw_grades = request.form['grades']
        try:
            grades = parse_grades(raw_grades)
            gpa = calculate_gpa(grades)
        except KeyError:
            return redirect('/', notice="Invalid grades")

        return render_template('gpa.html', gpa=gpa, courses=grades)
