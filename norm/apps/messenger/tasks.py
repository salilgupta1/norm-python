# from celery import task
# from itertools import izip

# import controller
# from .models import Response, Habit

# # @task()
# def send_reminders():
#     """
#     :return: void
#     """
#     habits = controller.get_habits()
#     if len(habits) > 0:
#         responses = controller.create_responses(habits)

#         for response, habit in izip(responses, habits):
#             generic = controller.create_generic_templates(response.id, habit.content)
#             controller.send_to_facebook(generic, FB_API_ENDPOINT, {'access_token':PAGE_ACCESS_TOKEN})
