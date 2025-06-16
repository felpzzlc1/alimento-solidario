from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<path:filename>")
def html_files(filename):
    if filename.endswith(".html"):
        return render_template(filename)
    return send_from_directory("static", filename)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)