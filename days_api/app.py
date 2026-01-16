"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })

def clear_history():
    """Clears the app history."""
    app_history.clear()

def validate_between_request_json(dict:dict) -> None:
    """raises error if keys aren't correct"""

    if set(dict.keys()) != {"first","last"}:
        raise ValueError({"error": True, "message": "Missing required data."})



def validate_request_json(dict: dict, keys:set[str]) -> None:
    """raises error if keys aren't correct"""

    if set(dict.keys()) != keys:
        raise ValueError({"error": True, "message": "Missing required data."})

def get_number(request) -> int:
    """Returns number of values to return for history"""

    args = request.args.to_dict()

    if args == {}:
        return 5
    
    if set(args.keys()) != {"number"}:
        raise ValueError({"error":True, "message":"message 1"}, 400)
    
    try:
        int(args["number"])
    except Exception:
        raise ValueError(
            {"error": "Number must be an integer between 1 and 20."}, 400)

    number = int(args["number"])

    if 1 <= number <= 20 :

        return number

    raise ValueError(
        {'error': 'Number must be an integer between 1 and 20.'}, 400)


def return_history_logs(number:int) -> list:

    if number == 0:
        return [{}]

    if number >= len(app_history):
        return app_history

    return app_history[:number]
    


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})

@app.post("/between")
def return_days_between():
    """Returns day between two dates entered"""

    first_last = request.json
    try:
        validate_between_request_json(first_last)

        first_date = first_last["first"]
        last_date = first_last["last"]

        first_date = convert_to_datetime(first_date)
        last_date = convert_to_datetime(last_date)

        days_between = get_days_between(first_date, last_date)

        add_to_history(request)

        return jsonify( {"days":days_between} ), 200
    
    except ValueError as e:
        return jsonify( {"error":f"{e.args[0]["message"]}"} ), 400
    
@app.post('/weekday')
def return_weekday():
    """Returns the name of the day of the week given"""

    day_of_week = request.json

    try:

        validate_request_json(day_of_week,{"date"})
        
        date = day_of_week["date"]
        date = convert_to_datetime(date)

        day_name = get_day_of_week_on(date)

        add_to_history(request)

        return jsonify({"weekday":day_name}), 200
    except ValueError as e:
        return jsonify({"error": f"{e.args[0]["message"]}"}), 400

@app.route("/history", methods = ["GET","DELETE"])
def return_response():

    if request.method == "POST":
        return jsonify([]), 404
    
    if request.method == "GET":

        print(request.args.to_dict())
        
        try:
            number = get_number(request)

            print(number,'number')

            logs = return_history_logs(number)

            if logs == []:
                return jsonify([{}]), 200
            return jsonify(logs), 200
            
        except ValueError as e:
            return jsonify(e.args[0]), e.args[1]
        except TypeError as e:
            return jsonify(e.args[0]), e.args[1]
    
    if request.method == "DELETE":

        clear_history()

        return jsonify({"status": "History cleared"}), 200
        
        


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
