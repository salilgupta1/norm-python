import os

from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import controller

# Create your views here.

class Webhook(APIView):

    def get(self, request, format='json'):
        """
        Authenticate bot
        """
        if request.query_params.get('hub.verify_token', False) == os.environ['VERIFY_TOKEN']:
            return HttpResponse(request.query_params['hub.challenge'])
        return Response(status=403)

    def post(self, request, format='json'):
        incoming_data = request.data
        print incoming_data
        for entry in incoming_data['entry']:
            response_data = controller.process_entry(entry)
            controller.send_to_facebook(response_data, url=os.environ['FB_ENDPOINT'], query_params={'access_token':os.environ['PAGE_ACCESS_TOKEN']})
        return Response(status=200)

