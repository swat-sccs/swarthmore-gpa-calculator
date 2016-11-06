from getpass import getpass
import requests
from random import choice, random
from sympy import Symbol, Subs
from sympy.solvers import solve
from sympy.functions import re

def parse_grades(raw_grades):
    """Convert from a string of grades to a structured dict.

    Args:
        raw_grades: A string containing the user's raw grades copied and pasted
            from MySwarthmore (hopefully)
    Returns:
        A list of dicts, one per course found while parsing raw_grades, with
        the fields:
        ['course', 'title', 'credits', 'grade', 'division', 'instructor']
    """
    # Split raw_grades up by line, remove column header lines and blank lines
    lines = raw_grades.split("\n")
    def is_course_line(line): 

        return line.strip() and \
               not(line.startswith("Term") or line.startswith("Course"))
    courses = list(filter(is_course_line, lines))

    # Convert each course row to a dict
    course_list = []
    for course in courses:
        course_info = course.split("\t") # Split up fields of row
        course_fields = ['course', 
                         'title', 
                         'credits', 
                         'grade', 
                         'division', 
                         'instructor'
                        ]
        if len(course_info) == len(course_fields):
            course_dict = dict(zip(course_fields, course_info))
            course_list.append(course_dict)

    return course_list


def calculate_gpa(course_list):
    """Given a list of course dicts, calculate the GPA.
    
    Args:
        course_list: A list of dicts, each corresponding to a course with fields
            ['course', 'title', 'credits', 'grade', 'division', 'instructor']

    Returns:
        A float representing the user's GPA, calculated from the inputted list
        of courses.
    """
    grade_point_equivs = {'A+': 4.0,
                          'A' : 4.0,
                          'A-': 3.67,
                          'B+': 3.33,
                          'B' : 3.0,
                          'B-': 2.67,
                          'C+': 2.33,
                          'C' : 2.0,
                          'C-': 1.67,
                          'D+': 1.33,
                          'D' : 1.0,
                          'D-': 0.67,
                          'F' : 0.0
                         }
    total_credits = 0
    total_grade_points = 0

    for course in course_list:
        credits = float(course['credits'])
        try:
            total_grade_points += credits * grade_point_equivs[course['grade']]
        except KeyError: # Skip if it's an invalid grade (e.g., CR/NR, W, 1)
            continue
        total_credits += credits

    return total_grade_points / total_credits


def construct_integral(gpa):
    """Constructs a definite integral which evaluates to the inputted GPA.

    Randomly chooses a and b values for a polynomial (poly) of the form
    ax^3 + bx^2 + cx, then chooses c based on a and b to ensure real solutions.
    Then calculates the upper bound of the definite integral of the derivative
    of poly with lower bound 0 such that the result is equal to gpa, and returns 
    the integral as a string in LaTeX format.
    
    Args:
        gpa: The GPA value for which to construct an integral.
    Returns:
        A LaTeX-formatting string containing the integral.
    """
    coeff_range = range(2, 10)
    offset_range = range(-5, 6)
    a = choice(coeff_range) / 4
    b = choice(coeff_range) / 3
    c = choice(coeff_range) / 2
    d = choice(offset_range)

    x = Symbol('x', real=True)
    poly = a * x**4 + b * x**3 + c * x**2 + d * x
    lo = min(solve(poly, x)) - round(random(), 3)
    up = max(solve(poly - poly.subs(x, lo) - gpa, x))

    return "\int_{" + ("%.3f" % lo) + "}^{" + ("%.3f" % up) + "}" + "(" + \
           str(int(a * 4)) + "x^3 " + int2sum_part(b * 3) + "x^2 " + \
           int2sum_part(c*2) + "x" + int2sum_part(d) + ")\,dx"


def int2sum_part(x):
    """
    Return a string of the form "+ x" if x is positive, "- x" if n is
    negative, or an empty string if x is 0 (for use in LaTeX formatting).
    """
    if x == 0:
        return ""
    operation = "- {}" if x < 0 else "+ {}"
    return operation.format(str(abs(int(x))))


# def scrape_courses():
    # url = 'https://myswat.swarthmore.edu/pls/twbkwbis.P_ValLogin'
    # username = input("Username: ")
    # password = getpass("Password: ")
    # payload = {
        # 'PIN': password,
        # 'sid': username
    # }
    # with requests.session() as s:
        # r = s.post(url, data=payload)
        # r = s.get('https://myswat.swarthmore.edu/pls/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu&msg=WELCOME://myswat.swarthmore.edu/pls/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu&msg=WELCOME+/')
        # print(r.text)
        # print(r.headers)
        # r.raise_for_status()


# # scrape_courses()

