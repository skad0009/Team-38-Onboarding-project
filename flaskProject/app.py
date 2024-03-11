from flask import Flask, request, render_template, request, jsonify
from uv_locator import get_uv_index, get_location
from uv_forecast import forecast_uv
import pandas as pd
import csv
import ast
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


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
            uv_index = get_uv_index(location)
            if uv_index is not None:
                # 如果成功获取到UV指数，返回JSON响应
                return jsonify({"location": location, "uv_index": uv_index}), 200
            else:
                # 如果没有获取到UV指数，返回错误消息
                return jsonify({"error": "UV index data not available"}), 404
        except Exception as e:
            # 处理任何可能发生的异常
            return jsonify({"error": str(e)}), 500
    else:
        # 如果没有提供location参数
        return jsonify({"error": "No location provided"}), 400


@app.route('/get_uv_forecast', methods=['GET'])
def get_uv_forecast():
    # 假设forecast_uv()返回所需的JSON数据
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
        "No Hat-Singlet-Half Pants": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",,
        "No Hat-Singlet-Short Skirt": "Apply 4 teaspoons  (20 ml) of sunscreen every two hours.",,
        "No Hat-Singlet-Swimsuit": "Apply 5 teaspoons (23 ml) of sunscreen every two hours.",,
        "No Hat-Swimsuit-Pants": "Apply 3 teaspoons (14 ml) of sunscreen every two hours.",
        "No Hat-Swimsuit-Half Pants": "Apply 4 teaspoons  (20 ml) of sunscreen every two hours.",,
        "No Hat-Swimsuit-Short Skirt": "Apply 5 teaspoons (23 ml)  of sunscreen every two hours.",,
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
        "Hat-Swimsuit-Swimsuit": "Apply 4 teaspoons (20 ml) of sunscreen every two hours.",
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

    clothing_map = {
    "1": {"Head": "No Hat", "Torso": "Full Sleeve Top", "Lower Body": "Pants"},
    "2": {"Head": "No Hat", "Torso": "Full Sleeve Top", "Lower Body": "Half Pants"},
    "3": {"Head": "No Hat", "Torso": "Full Sleeve Top", "Lower Body": "Short Skirt"},
    "4": {"Head": "No Hat", "Torso": "Full Sleeve Top", "Lower Body": "Swimsuit"},
    "5": {"Head": "No Hat", "Torso": "Half Sleeve Top", "Lower Body": "Pants"},
    "6": {"Head": "No Hat", "Torso": "Half Sleeve Top", "Lower Body": "Half Pants"},
    "7": {"Head": "No Hat", "Torso": "Half Sleeve Top", "Lower Body": "Short Skirt"},
    "8": {"Head": "No Hat", "Torso": "Half Sleeve Top", "Lower Body": "Swimsuit"},
    "9": {"Head": "No Hat", "Torso": "Singlet", "Lower Body": "Pants"},
    "10": {"Head": "No Hat", "Torso": "Singlet", "Lower Body": "Half Pants"},
    "11": {"Head": "No Hat", "Torso": "Singlet", "Lower Body": "Short Skirt"},
    "12": {"Head": "No Hat", "Torso": "Singlet", "Lower Body": "Swimsuit"},
    "13": {"Head": "No Hat", "Torso": "Swimsuit", "Lower Body": "Pants"},
    "14": {"Head": "No Hat", "Torso": "Swimsuit", "Lower Body": "Half Pants"},
    "15": {"Head": "No Hat", "Torso": "Swimsuit", "Lower Body": "Short Skirt"},
    "16": {"Head": "No Hat", "Torso": "Swimsuit", "Lower Body": "Swimsuit"},
    "17": {"Head": "Hat", "Torso": "Full Sleeve Top", "Lower Body": "Pants"},
    "18": {"Head": "Hat", "Torso": "Full Sleeve Top", "Lower Body": "Half Pants"},
    "19": {"Head": "Hat", "Torso": "Full Sleeve Top", "Lower Body": "Short Skirt"},
    "20": {"Head": "Hat", "Torso": "Full Sleeve Top", "Lower Body": "Swimsuit"},
    "21": {"Head": "Hat", "Torso": "Half Sleeve Top", "Lower Body": "Pants"},
    "22": {"Head": "Hat", "Torso": "Half Sleeve Top", "Lower Body": "Half Pants"},
    "23": {"Head": "Hat", "Torso": "Half Sleeve Top", "Lower Body": "Short Skirt"},
    "24": {"Head": "Hat", "Torso": "Half Sleeve Top", "Lower Body": "Swimsuit"},
    "25": {"Head": "Hat", "Torso": "Singlet", "Lower Body": "Pants"},
    "26": {"Head": "Hat", "Torso": "Singlet", "Lower Body": "Half Pants"},
    "27": {"Head": "Hat", "Torso": "Singlet", "Lower Body": "Short Skirt"},
    "28": {"Head": "Hat", "Torso": "Singlet", "Lower Body": "Swimsuit"},
    "29": {"Head": "Hat", "Torso": "Swimsuit", "Lower Body": "Pants"},
    "30": {"Head": "Hat", "Torso": "Swimsuit", "Lower Body": "Half Pants"},
    "31": {"Head": "Hat", "Torso": "Swimsuit", "Lower Body": "Short Skirt"},
    "32": {"Head": "Hat", "Torso": "Swimsuit", "Lower Body": "Swimsuit"}
}


    selections = {
        "Head": clothing_map.get(headwear, {}).get("Head", "No Hat"),
        "Torso": clothing_map.get(topwear, {}).get("Torso", "Singlet"),
        "Lower Body": clothing_map.get(bottomwear, {}).get("Lower Body", "Pants")
    }

    print("Mapped Selections:", selections)
    print("Inputs:", headwear, topwear, bottomwear, uv_index)
    advice = sunscreen_advice(selections, uv_index)
    return jsonify({"result": advice})


if __name__ == '__main__':
    app.run(debug=True)
