from getpass import getpass
import requests
from random import randint
from sympy import Symbol, diff, Integral, Subs
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
    
    Args:
        gpa: The GPA value for which to construct an integral.
    Returns:
        A dict containing the relevant information about the integral
    """
    # TODO: desccribe returned dict in docstring
    a = randint(2, 9)
    b = randint(2, 9)
    c = (b**2) // (4 * a) - 5

    x = Symbol('x')
    poly = a * x**3 + b * x**2 + c * x
    up = max([re(n) for n in solve(poly - gpa, x)]) # Solution

    return {'a': 3*a,
            'b': 2*b,
            'c': c,
            'lo': 0,
            'up': up}
    

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

