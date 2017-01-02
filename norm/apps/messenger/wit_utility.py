import time

def send(request, response):
	pass

def save_habit(response):
	pass

def merge(request, response):
	pass

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

def create_session_id():
    return hex(int(time()*1000))[2:]

actions = {
	'send':send,
	'merge': merge,
	'saveHabit': save_habit
}