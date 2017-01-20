from __future__ import absolute_import, unicode_literals
from itertools import izip
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

import norm.apps.messenger.controller as controller
import norm.apps.messenger.fb as fb

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='0', hour='*')),
    name='send_reminders',
    ignore_results=True
)
def send_reminders():
    """
    :return: void
    """

    logger.info('gonna send some reminders')

    habits = controller.get_habits()
    if len(habits) > 0:
        responses = controller.create_responses(habits)
        logger.info('we got some reminders')

        for response, habit in izip(responses, habits):
            generic = fb.create_generic_templates(response.id, habit.content)
            fb.send_to_messenger(response.recipient_id, generic)