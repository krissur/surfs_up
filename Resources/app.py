from flask import Flask
app = Flask(__name__)
# the '/' inside the parentheses, this indicates the root of routes- the begining
@app.route('/')
def hello_world():
    return 'Hello world'
