from flask import Flask

application = Flask(__name__)
application.config.from_object(__name__)
application.secret_key = 'HolyHandGrenade'

