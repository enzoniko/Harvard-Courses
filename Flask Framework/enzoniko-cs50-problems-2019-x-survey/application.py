import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    print(request.form.get("name"), request.form.get("sport"))

    # if no values, return error.
    if request.form.get("name") == "" or request.form.get("sport") == "":
        message = "You need to provide a name and a sport."
        return render_template("error.html", message=message)
    with open("./survey.csv", "a") as f:
        csv_f = csv.writer(f, delimiter=",")
        csv_f.writerow([request.form.get('name'),
                        request.form.get('sport')])
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    submits = []
    with open("./survey.csv", "r") as f:
        csv_f = csv.reader(f)
        for row in csv_f:
            submits.append(row)
    return render_template("sheet.html", submits=submits)
    # return render_template("error.html", message="TODO")

