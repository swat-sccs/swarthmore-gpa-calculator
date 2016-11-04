from getpass import getpass
import requests

def parse_grades(raw_grades):
    """Convert from a string of grades to a structured dict.

    Args:
        raw_grades
    Returns
    """
    # Split raw data up by line, and filter out column label lines
    lines = raw_grades.split("\n")
    is_course_line = lambda l: not (l.startswith("Term") or l.startswith("Course"))
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
        course_dict = dict(zip(course_fields, course_info))
        course_list.append(course_dict)

    return course_list


def calculate_gpa(course_list):
    """Given a list of course dicts, calculate the GPA."""
    gpa_equivs = {'A+': 4.0,
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
                  'F' : 0.0}
    total_credits = 0
    equiv_sum = 0

    for course in course_list:
        credits = float(course['credits'])
        try:
            equiv_sum += credits * gpa_equivs[course['grade']]
        except KeyError: # Skip if it's an invalid grade (e.g., CR/NR, W, 1)
            continue
        total_credits += credits

    return equiv_sum / total_credits


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

