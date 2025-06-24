import logging
import flask
from flask import request
from logging.handlers import RotatingFileHandler

log_format = logging.Formatter('%(asctime)s %(message)s')

record_logs = logging.getLogger('web_logs')
record_logs.setLevel(logging.INFO)
record_handler = RotatingFileHandler('web_records.log', maxBytes=2000, backupCount=20)
record_handler.setFormatter(log_format)
record_logs.addHandler(record_handler)

def web_honeypot(inp_username="admin", inp_password="password"):
    app = flask.Flask(__name__)

    @app.route('/')
    def index():
        return flask.render_template('webpage.html')  # Ensure the 'webpage.html' exists in templates folder

    @app.route('/webpage-login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']
        ip_address = request.remote_addr

        record_logs.info(f'IP Address {ip_address}, Username:{username}, Password:{password}')

        if username == inp_username and password == inp_password:
            return 'Robovitics'
        else:
            return "Invalid username or password. Please try again."

    return app

def initiate(port=2666, inp_username="admin", inp_password="password"):
    web_app = web_honeypot(inp_username, inp_password)
    web_app.run(debug=True, port=port, host="0.0.0.0")  

initiate(port=2666, inp_username="admin", inp_password="password")
