import time
import fb
import controller

def send(request, response):
    """
    Wit AI wrapper for sending messages to fb
    """
    fb.send_to_messenger(request['session_id'], response['text'])

def save_habit(request):
    context = request['context']
    entities = request['entities']

    if 'when' in context:
        del context['when']
    if 'meridian' in context:
        del context['meridian']

    when = first_entity_value(entities, 'when')
    if when:
        context['when'] = when

    meridian = first_entity_value(entities, 'meridian')
    if meridian:
        context['meridian'] = meridian

    hour = controller.convert_to_military(when, meridian)
    user_timezone = fb.get_fb_user_timezone(request['session_id'])
    hour = controller.convert_to_gmt(user_timezone, hour)
    controller.create_habit(context['habit'], request['session_id'], hour)

    return context

def merge(request):
    context = request['context']
    entities = request['entities']

    if 'reminder' in context:
        del context['reminder']
    reminder = first_entity_value(entities, 'reminder')
    if reminder:
        context['habit'] = reminder

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

# def create_session_id():
#     return hex(int(time()*1000))[2:]

actions = {
    'send':send,
    'merge': merge,
    'saveHabit': save_habit
}