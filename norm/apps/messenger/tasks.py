import os
from __future__ import absolute_import, unicode_literals
from itertools import izip
from celery.task.schedules import crontab
from celery.decorators import periodic_task

import controller
from models import Response, Habit

@periodic_task(
    run_every=(crontab(minute=0, hour="*")),
    name='send_reminders',
    ignore_results=True
)
def send_reminders():
    """
    :return: void
    """
    habits = controller.get_habits()
    if len(habits) > 0:
        responses = controller.create_responses(habits)

        for response, habit in izip(responses, habits):
            generic = controller.create_generic_templates(response.id, habit.content)
            controller.send_to_facebook(generic, os.environ['FB_ENDPOINT'], {'access_token':os.environ['PAGE_ACCESS_TOKEN']})
