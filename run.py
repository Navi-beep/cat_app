from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_cat():
    return "<p>Hello, Cat!</p>"

