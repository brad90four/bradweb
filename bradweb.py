from string import capwords

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.jinja")


@app.route("/bradzone")
def bradzone():
    return render_template("bradzone.jinja")


@app.route("/<name>")
def user(name):
    name = capwords(name)
    if len(name) > 40:
        name = name[0:39]
    return render_template("name.jinja", name=name)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        return redirect(url_for("user", name=user))
    else:
        return render_template("login.jinja")


if __name__ == "__main__":
    app.run()
