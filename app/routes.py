from app import app


@app.route("/")
def hello_cat():
    return "Hello, Cat!"