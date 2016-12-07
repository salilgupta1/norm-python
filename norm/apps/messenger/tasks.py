# from celery import task
# from itertools import izip

# import controller
# from .models import Response, Habit

# FB_API_ENDPOINT = 'https://graph.facebook.com/v2.6/me/messages'
# PAGE_ACCESS_TOKEN = 'EAAZAurP9vHZA0BAFTJkaBNa0agVoZC2L8VqTrJqxvlikssLfZA9IoG3AGJZCERKAtRyOGOlxbMAt9nqNkbAcjx9ZC63rUOD42Q4q2ZAX34ssEHQ5YgO3HR6o4rGFod3D5CSQoonodExOHAjEYs0lNnkLJxKcf2VZCZBFzQZAdKFiRPwgZDZD'


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
