import requests
import os
import json

import controller
import wit_utility


def get_fb_user_timezone(fb_user_id):
    url = 'https://graph.facebook.com/v2.6/{}'.format(str(fb_user_id))
    query_params = {'fields':'timezone'}

    response = requests.get(url, params=query_params)

def send_to_messenger(data):
    """
    :param: data: dict
    :return: status Integer
    """
    url = os.environ['FB_ENDPOINT']
    query_params = {'access_token':os.environ['PAGE_ACCESS_TOKEN']}
    return requests.post(url, json=data, params=query_params)

def process_entry(entry):
    """
    Processes the entry dictionary 
    :param: entry: dict
    """
    response = {}
    log(entry)
    for messaging in entry['messaging']:
        fb_id = messaging['sender']['id']
        if 'postback' in messaging:
       		response['message'] = {'text': self._process_postback(messaging['postback'])}
        	response['recipient'] = {'id': fb_id}
        	self.send_to_messenger(response)
        else:
            self._process_user_message(messaging, fb_id)
        

def _process_postback(postback):
    """
    Specifically for collecting a response from a reminder
    :param: postback: dict
    return text_response str
    """
    payload = json.loads(postback['payload'])
    response_id = payload['response_id']
    answer = payload['answer']
    
    # not ideal place to put this but w.e.
    controller.save_user_response(response_id, answer)
    
    return 'Good Job!!' if answer == 'Yes' else 'Oh Poop ...'

def _process_message(message, fb_id):
	"""
	Wit API endpoint that will deal with all message processing
	:param: message str
	:param: fb_id str
	"""
	client = Wit(access_token=os.environ['WIT_TOKEN'], actions=wit_utility.actions)

	session_id = fb_id + '-{}'.format(wit_utility.create_session_id())
	client.run_actions(session_id=session_id, message=message)

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