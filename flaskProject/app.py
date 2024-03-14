from flask import Flask, request, render_template, jsonify, redirect, flash
from uv_locator import get_uv_index, get_location
from uv_forecast import forecast_uv
import datetime as dt

app = Flask(__name__)
app.secret_key = '123456'

# 假设的正确密码
CORRECT_PASSWORD = '123456'


@app.route('/')
def hello_world():  # put application's code here
    return render_template('login.html')


@app.route('/verify_password', methods=['POST'])
def verify_password():
    password = request.form['password']
    # verify password
    if password == CORRECT_PASSWORD:
        # If the password is correct, redirect to the US1.1 page
        return redirect('/us1')
    else:
        # If the password is incorrect, display the error message and reload the login page
        flash('Wrong password, please re-enter！')
        return redirect('/')


# display the us1.1 html
@app.route('/us1')
def us1():
    return render_template('US1.1.html')


# display the us1.4 html
@app.route('/us4')
def us4():
    return render_template('US1.4.html')


# US 1.1 REST API
@app.route('/uv_index', methods=['GET'])
def uv_index():
    location = request.args.get("location")
    if location:
        try:
            uv_index, curr_timestamp = get_uv_index(location)
            if uv_index is not None:
                # Convert UNIX timestamp to readable date time format
                readable_time = dt.datetime.fromtimestamp(curr_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                # If the UV index is successfully obtained, return a JSON response
                return jsonify({"location": location, "uv_index": uv_index, "timestamp": readable_time}), 200
            else:
                # If the UV index is not obtained, return an error message
                return jsonify({"error": "UV index data not available"}), 404
        except Exception as e:
            # Handle any exceptions that may occur
            return jsonify({"error": str(e)}), 500
    else:
        # If no location parameter is provided
        return jsonify({"error": "No location provided"}), 400


@app.route('/get_uv_forecast', methods=['GET'])
def get_uv_forecast():
    forecast_data = forecast_uv(debug = False)
    return jsonify(forecast_data)


# -----------------------------------------------------------------
def key(selections):
    return '-'.join(selections.values())


def sunscreen_advice(selections, uv_index):
    advice_combinations = {
        "No Hat-Full Sleeve Top-Pants": "Apply 1 teaspoon (4 ml) of sunscreen every two hours.",
        "No Hat-Full Sleeve Top-Half Pants": "Apply 2.5 teaspoons (11 ml)  of sunscreen every two hours.",
        "No Hat-Full Sleeve Top-Short Skirt": "Apply 3  teaspoons (14 ml) of sunscreen every two hours.",
        "No Hat-Full Sleeve Top-Swimsuit": "Apply 4 teaspoons  (20 ml) of sunscreen every two hours.",
        "No Hat-Half Sleeve Top-Pants": "Apply 1.5 teaspoons (6 ml) of sunscreen every two hours.",
        "No Hat-Half Sleeve Top-Half Pants": "Apply 2.5 teaspoons (11 ml)  of sunscreen every two hours.",
        "No Hat-Half Sleeve Top-Short Skirt": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",
        "No Hat-Half Sleeve Top-Swimsuit": "Apply 5 teaspoons (23 ml) of sunscreen every two hours.",
        "No Hat-Singlet-Pants": "Apply 2 teaspoons (10 ml) of sunscreen every two hours.",
        "No Hat-Singlet-Half Pants": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",
        "No Hat-Singlet-Short Skirt": "Apply 4 teaspoons  (20 ml) of sunscreen every two hours.",
        "No Hat-Singlet-Swimsuit": "Apply 5 teaspoons (23 ml) of sunscreen every two hours.",
        "No Hat-Swimsuit-Pants": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",
        "No Hat-Swimsuit-Half Pants": "Apply 4 teaspoons  (20 ml) of sunscreen every two hours.",
        "No Hat-Swimsuit-Short Skirt": "Apply 5 teaspoons (23 ml)  of sunscreen every two hours.",
        "No Hat-Swimsuit-Swimsuit": "Apply 6 teaspoons (30 ml) of sunscreen every two hours.",
        "Hat-Full Sleeve Top-Pants": "Apply 1 teaspoon (4 ml) of sunscreen every two hours.",
        "Hat-Full Sleeve Top-Half Pants": "Apply 2 teaspoons (10 ml)  of sunscreen every two hours.",
        "Hat-Full Sleeve Top-Short Skirt": "Apply 2.5 teaspoons (11 ml) of sunscreen every two hours.",
        "Hat-Full Sleeve Top-Swimsuit": "Apply 4 teaspoons (20 ml) of sunscreen every two hours.",
        "Hat-Half Sleeve Top-Pants": "Apply 1.5 teaspoons (6 ml) of sunscreen every two hours.",
        "Hat-Half Sleeve Top-Half Pants": "Apply 2.5 teaspoons (11 ml) of sunscreen every two hours.",
        "Hat-Half Sleeve Top-Short Skirt": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",
        "Hat-Half Sleeve Top-Swimsuit": "Apply 4.5 teaspoons (21 ml) of sunscreen every two hours.",
        "Hat-Singlet-Pants": "Apply 2 teaspoons (10 ml) of sunscreen every two hours.",
        "Hat-Singlet-Half Pants": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",
        "Hat-Singlet-Short Skirt": "Apply 3.5 teaspoons (7ml) of sunscreen every two hours.",
        "Hat-Singlet-Swimsuit": "Apply 5 teaspoons (23 ml) of sunscreen every two hours.",
        "Hat-Swimsuit-Pants": "Apply 1 teaspoon (4 ml) of sunscreen every two hours.",
        "Hat-Swimsuit-Half Pants": "Apply 2 teaspoons (10 ml) of sunscreen every two hours.",
        "Hat-Swimsuit-Short Skirt": "Apply 2.5 teaspoons (11 ml) of sunscreen every two hours.",
        "Hat-Swimsuit-Swimsuit": "Apply 4 teaspoons (20 ml) of sunscreen every two hours."
    }

    advice_key = key(selections)
    advice = advice_combinations.get(advice_key, "Please ensure to wear sunscreen!")

    if int(uv_index) > 2:
        return advice
    else:
        return "UV index is low, but still consider wearing sunscreen."


# US 1.4 REST API
@app.route('/calculate_sunscreen', methods=['GET'])
# You can get front-end data and write back-end logic here
def calculate_sunscreen():
    # input 1
    headwear = request.args.get("input1")

    # input 2
    topwear = request.args.get("input2")

    # input 3
    bottomwear= request.args.get("input3")

    # input 4
    uv_index = request.args.get("input4")
    headwear_options = {"1": "No Hat", "2": "Hat"}
    topwear_options = {"1": "Full Sleeve Top", "2": "Half Sleeve Top", "3": "Singlet", "4": "Swimsuit"}
    bottomwear_options = {"1": "Pants", "2": "Half Pants", "3": "Short Skirt", "4": "Swimsuit"}

    # Map the inputs to their descriptive strings
    selections = {
        "Head": headwear_options.get(headwear, "No Hat"),
        "Torso": topwear_options.get(topwear, "Singlet"),
        "Lower Body": bottomwear_options.get(bottomwear,"Pants")
}

    print("Mapped Selections:", selections)
    print("Inputs:", headwear, topwear, bottomwear, uv_index)
    advice = sunscreen_advice(selections, uv_index)
    return jsonify({"result": advice})


if __name__ == '__main__':
    app.run(debug=True)
