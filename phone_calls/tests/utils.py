from phone_calls.core.models import PhoneRecord

_phone_call_id = 0


def make_timestamp(**kwargs):
    data = {'year': 2016, 'month': 2, 'day': 29, 'hour': 12, 'minute': 0, 'second': 0}
    data.update(kwargs)
    return '%s-%02d-%02dT%02d:%02d:%02dZ' % (data['year'], data['month'], data['day'],
                                             data['hour'], data['minute'], data['second'])


def create_phone_call(time_stamp, **kwargs):
    global _phone_call_id
    data = {'id': _phone_call_id, 'type': 'start', 'time_stamp': time_stamp, 'call_id': 70,
            'source': '5512345678', 'destination': '44123456789'}
    _phone_call_id += 1
    data.update(kwargs)
    return PhoneRecord.objects.create(**data)
