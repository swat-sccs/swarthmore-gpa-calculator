# WSGI file for Gwaihir deployment
import sys
sys.path.insert(0, './gpacalc')

from gpa_calc import app as application
