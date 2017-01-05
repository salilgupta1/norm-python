import json
import datetime
import sys

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
    :param: hour
    """
    habit = Habit(recipient_id, content)
    habit.save()
    schedule = Schedule(habit.id, hour)
    schedule.save()

### utility functions
def log(message):
    print str(message)
    sys.stdout.flush()

def convert_to_gmt(user_timezone, time):
    """
    :param: user_timezone Integer
    :param: time Integer
    return Integer
    """
    return (time + user_timezone) % 24

def convert_to_military(time, meridian):
    """
    :param: time Integer
    :param: meridian str
    :return: Integer
    """
    if meridian.upper() == 'PM':
        time += 12
    return time





