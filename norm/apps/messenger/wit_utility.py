import time
import fb
import controller

def send(request, response):
    """
    Wit AI wrapper for sending messages to fb
    """
    fb_id = get_fb_id_from_session_id(request['session_id'])
    fb.send_to_messenger(fb_id, {'text':response['text']})

def save_habit(request):
    context = request['context']
    entities = request['entities']

    habit = first_entity_value(entities, 'reminder')
    date_time = first_entity_value(entities, 'datetime')

    if habit:
        context['habit'] = habit

    # We are assuming that the user will
    # include the datetime. That's why i'm not worried about not hitting this if statement ...
    if date_time:
        hour, military_hour = controller.extract_hour(date_time)
        context['hour'] = hour

    fb_id = get_fb_id_from_session_id(request['session_id'])
    user_timezone = fb.get_fb_user_timezone(fb_id)

    military_hour = controller.convert_to_gmt(user_timezone, military_hour)
    controller.create_habit(context['habit'], fb_id, military_hour)
    delete_session_id(fb_id)

    return context

def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def find_or_create_session_id(fb_id):
    """
    Searches a global dictionary called sessions
    Not a long term solution but doable for now
    :param: fb_id str
    return str
    """
    if sessions.get(fb_id) is None:
        unique_id = hex(int(time.time()*1000))[2:]
        sessions[fb_id] = fb_id + '-{}'.format(unique_id)
    return sessions[fb_id]

def delete_session_id(fb_id):
    del sessions[fb_id]

def get_fb_id_from_session_id(session_id):
    return session_id.split('-')[0]

sessions = {}
actions = {
    'send':send,
    'saveHabit': save_habit
}