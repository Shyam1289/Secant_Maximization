from flask import Flask,jsonify
from secant import run_secant_method

app = Flask(__name__)

@app.route("/",methods = ["GET"])
def home():
    return jsonify({"message": "Secant Method API is runnning!"})

@app.route("/run", methods = ["POST"])
def run():
    results = run_secant_method()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug = True)