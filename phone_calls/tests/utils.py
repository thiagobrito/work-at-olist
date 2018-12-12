from rest_framework.reverse import reverse

_phone_call_id = 1


def make_timestamp(**kwargs):
    data = {'year': 2016, 'month': 2, 'day': 29, 'hour': 12, 'minute': 0, 'second': 0}
    data.update(kwargs)
    return '%s-%02d-%02dT%02d:%02d:%02dZ' % (data['year'], data['month'], data['day'],
                                             data['hour'], data['minute'], data['second'])


def make_phone_call(client, time_stamp, **kwargs):
    data = {'type': 'start', 'time_stamp': time_stamp,
            'call_id': 70, 'source': '5512345678', 'destination': '44123456789'}
    data.update(kwargs)
    return client.post(reverse('phone_record-list'), data, format='json')
