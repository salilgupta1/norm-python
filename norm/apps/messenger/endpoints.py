import os

from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import controller

# Create your views here.

class Webhook(APIView):
    FB_API_ENDPOINT = 'https://graph.facebook.com/v2.6/me/messages'
    PAGE_ACCESS_TOKEN = 'EAAZAurP9vHZA0BAFTJkaBNa0agVoZC2L8VqTrJqxvlikssLfZA9IoG3AGJZCERKAtRyOGOlxbMAt9nqNkbAcjx9ZC63rUOD42Q4q2ZAX34ssEHQ5YgO3HR6o4rGFod3D5CSQoonodExOHAjEYs0lNnkLJxKcf2VZCZBFzQZAdKFiRPwgZDZD'

    def get(self, request, format='json'):
        """
        Authenticate bot
        """
        if request.query_params.get('hub.verify_token', False) == 'VERIFY_ME':
            return HttpResponse(request.query_params['hub.challenge'])
        return Response(status=403)

    def post(self, request, format='json'):
        incoming_data = request.data
        print incoming_data
        for entry in incoming_data['entry']:
            response_data = controller.process_entry(entry)
            controller.send_to_facebook(response_data, url=Webhook.FB_API_ENDPOINT, query_params={'access_token':Webhook.PAGE_ACCESS_TOKEN})
        return Response(status=200)

