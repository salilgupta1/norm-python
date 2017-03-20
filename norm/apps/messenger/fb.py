import os
import sys

import json
import requests
import wit

import controller
import wit_utility

client = wit.Wit(access_token=os.environ['WIT_TOKEN'], actions=wit_utility.actions)

def get_fb_user_timezone(fb_id):
    """
    :param: fb_id Integer
    return timezone Integer
    """
    url = 'https://graph.facebook.com/v2.6/{}'.format(str(fb_id))
    query_params = {
        'fields':'timezone',
        'access_token': os.environ['PAGE_ACCESS_TOKEN']
    }

    response = requests.get(url, params=query_params).json()
    return response['timezone']


def send_to_messenger(recipient_id, message):
    """
    :param: recipient_id: Integer
    :param: message: dictionary
    return void
    """

    data = {
        'recipient': {'id': recipient_id},
        'message': message
    }

    query_params = {
        'access_token':os.environ['PAGE_ACCESS_TOKEN']
    }

    url = 'https://graph.facebook.com/v2.6/me/messages'
    requests.post(url, json=data, params=query_params)

def process_entry(entry):
    """
    Processes the entry dictionary
    :param: entry: dict
    return void
    """
    # debug code
    # controller.log(entry)

    for messaging in entry['messaging']:
        fb_id = messaging['sender']['id']

        if 'postback' in messaging:
            message = { 'text': _process_postback(messaging['postback']) }
            send_to_messenger(fb_id, message)
        else:
            # wit_ai
            _process_user_message(messaging['message']['text'], fb_id)

def _process_postback(postback):
    """
    Specifically for collecting a response from a reminder
    :param: postback: dict
    return text_response str
    """
    payload = json.loads(postback['payload'])

    # not ideal place to put this but w.e.
    controller.save_user_response(payload['response_id'], payload['answer'])
    return 'Good Job!!' if answer == 'Yes' else 'Oh Poop ...'

def _process_user_message(message, fb_id):
    """
    Wit API endpoint that will deal with all message processing
    :param: message str
    :param: fb_id str
    """
    session_id = wit_utility.find_or_create_session_id(fb_id)
    try:
        client.run_actions(session_id=session_id, message=message)
    except:
        controller.log(sys.exc_info())

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
