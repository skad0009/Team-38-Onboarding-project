from flask import Flask, request, render_template,request

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
# You can get front-end data and write back-end logic here
def uv_index():
    location = request.args.get("location")
    print(location)
    return location


# US 1.4 REST API
@app.route('/calculate_sunscreen', methods=['GET'])
# You can get front-end data and write back-end logic here
def calculate_sunscreen():
    # input 1
    value1 = request.args.get("input1")

    # input 2
    value2 = request.args.get("input2")

    # input 3
    value3 = request.args.get("input3")

    # input 4
    value4 = request.args.get("input4")
    print(value1, value2, value3, value4)
    return f"result: {value1}, {value2}, {value3}, {value4}"


if __name__ == '__main__':
    app.run(debug=True)
