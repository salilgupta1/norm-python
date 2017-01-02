import os

from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

import fb

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
        for entry in incoming_data['entry']:
            response_data = fb.process_entry(entry)
        return Response(status=200)

