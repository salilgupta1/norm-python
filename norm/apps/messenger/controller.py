import json
import datetime
import sys
import re

from time import time
from models import Habit, Response, Schedule

def save_user_response(response_id, answer):
    """
    :param: response_id: Integer
    :param: answer: str
    :return: void
    """
    response = Response.objects.get(id=response_id)
    response.response_content = answer
    response.save(force_update=True)

def get_habits():
    """
    :return: [Habit]
    """
    hour = datetime.datetime.now().hour
    habits = Habit.objects.filter(schedule__hour=hour)
    return habits

def create_responses(habits):
    """
    :param: habits: [Habit]
    :return: responses
    """
    responses = []
    for habit in habits:
        response = Response(recipient_id=habit.recipient_id, habit_id=habit)
        responses.append(response)

    Response.objects.bulk_create(responses)
    return responses

def create_habit(content, recipient_id, hour):
    """
    Creates a habit and the appropriate schedule object
    :param: content str
    :param: recipient_id Integer
    :param: hour Integer
    """
    habit = Habit(recipient_id=recipient_id, content=content)
    habit.save()
    schedule = Schedule(habit_id=habit, hour=hour)
    schedule.save()

### utility functions
def log(message):
    print str(message)
    sys.stdout.flush()

def convert_to_gmt(user_timezone, hour):
    """
    :param: user_timezone Integer
    :param: hour Integer
    return Integer
    """
    return (hour - user_timezone) % 24

def extract_hour(date_time_str):
    """
    :param: date_time_str str
    :return: (hour:str, military_hour:int)
    """
    military_hour = int(re.search('T(\d+)[^:]*', date_time_str).group(1))
    if military_hour > 12:
        hour = military_hour - 12
        hour = str(hour) + 'pm'
    else:
        hour = str(military_hour) + 'am'
    return hour, military_hour
