"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Converts date string in the form 'day.month.year' to tuple"""

    # error handling
    try:
        date = datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Unable to convert value to datetime.")

    return date

def get_days_between(first: datetime, last: datetime) -> int:
    """Returns number of days between first and last"""

    if not( isinstance(first, datetime) and isinstance(last, datetime)):
        raise TypeError("Datetimes required.")

    date_difference = last - first

    return date_difference.days

def get_day_of_week_on(date_val: datetime) -> str:
    """Returns full day of the week given datetime object"""

    if not isinstance(date_val, datetime):
        raise TypeError("Datetime required.")
    
    day = datetime.strftime(date_val, "%A")

    return day


def get_current_age(birthdate: date) -> int:
    """Returns a person's current age given their birthday"""

    if not isinstance(birthdate, date):
        raise TypeError("Date required.")
    
    today = date.today()

    current_year = today.year
    current_month = today.month
    current_day = today.day
    
    year_difference = current_year - birthdate.year
    month_difference = (current_month - birthdate.month)%12
    day_difference = current_day - birthdate.day

    if day_difference < 0:
        month_difference -= 1
    if month_difference < 0:
        year_difference -= 1
    
    return year_difference
