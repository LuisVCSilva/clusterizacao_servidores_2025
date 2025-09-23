from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/alive")
def alive():
    return 'OK'


@app.route("/ready")
def ready():
    return jsonify(
        backend='ready',
        db='ready',
        queue='ready'
    )
