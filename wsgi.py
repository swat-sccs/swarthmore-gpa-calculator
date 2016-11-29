# WSGI file for Gwaihir deployment
import sys
sys.path.insert(0, '/srv/Secure/gpacalc')

from gpa_calc import app as application
