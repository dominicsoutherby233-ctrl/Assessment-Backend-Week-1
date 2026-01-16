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
    
    for value in dict.values():
        value = str(value)
        if len(value) != 10 or value[2] != "." or value[5] != ".":
            raise ValueError(
                {"error": True, "message": "Unable to convert value to datetime."})


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

        first_date = datetime.strptime(first_date, "%d.%m/%Y")
        last_date = datetime.strptime(last_date, "%d.%m/%Y")

        days_between = get_days_between(first_date, last_date)

        return jsonify( {"days":days_between} )
    except ValueError as e:
        return jsonify( {"error":f"{e.args[0]["message"]}"} ), 400
    



if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
