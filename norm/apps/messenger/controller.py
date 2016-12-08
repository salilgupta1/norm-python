import requests
import json
import datetime
from models import Habit, Response, Schedule

def send_to_facebook(data, url, query_params):
    """
    :param: data: dict
    :param: url: str
    :param: query_params: dict
    :return: status Integer
    """
    return requests.post(url, json=data, params=query_params)

def process_entry(entry):
    """
    :param: entry: dict
    return response_data: dict
    """
    response = {}
    for messaging in entry['messaging']:
        fb_id = messaging['sender']['id']
        response['recipient'] = {'id': fb_id}

        if 'message' in messaging:
            # for now just return back what was written
            # needs to handle creating a habit
            message_text = messaging['message']['text']
            response['message'] = {'text':message_text}
        elif 'postback' in messaging:
            response_id = messaging['postback']['payload']['response_id']
            answer = messaging['postback']['payload']['answer']

            if answer == 'Yes':
                response['message'] = {'text': 'Good Job!!'}
            else:
                response['message'] = {'text': 'Oh Poop....'}

            _save_user_response(response_id, answer)

    return response

def _save_user_response(response_id, answer):
    """
    :param: response_id: Integer
    :param: answer: str
    :return: void
    """
    response = Response(id=response_id, response_content=answer)
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
        response = Response(recipient_id=habit.recipient_id, habit_id=habit.id)
        responses.append(response)

    Response.objects.bulk_create(responses)
    return responses

def create_generic_templates(response_id, content):
    """
    :param: response_id: Integer
    :param: content: str
    :return: template: dictionary
    """
    yes_payload = json.dumps({'response_id': response_id, 'answer':'Yes'})
    no_payload = json.dumps({'response_id': response_id, 'answer':'No'})

    template = {
        'attachment': {
            'type':'template',
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'Reminder',
                        'subtitle': content,
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Yes',
                                'payload': yes_payload
                            },
                            {
                                'type': 'postback',
                                'title': 'No',
                                'payload': no_payload
                            }
                        ]
                    }
                ]
            }
        }
    }

    return template
