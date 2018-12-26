'''
Insert the following calls to your app after it is deployed to a working environment (eg. Heroku, gigalixir).
This sample data will be used in your evaluation, so do this as the last step before submitting the project.

The following phone calls have been made from the number 99 98852 6423 to 99 3346 8278 (whitespaces are used here only
for readability purposes, the phone numbers formats have been specified on a previous section).

call_id: 70, started at 2016-02-29T12:00:00Z and ended at 2016-02-29T14:00:00Z.
call_id: 71, started at 2017-12-11T15:07:13Z and ended at 2017-12-11T15:14:56Z.
call_id: 72, started at 2017-12-12T22:47:56Z and ended at 2017-12-12T22:50:56Z.
call_id: 73, started at 2017-12-12T21:57:13Z and ended at 2017-12-12T22:10:56Z.
call_id: 74, started at 2017-12-12T04:57:13Z and ended at 2017-12-12T06:10:56Z.
call_id: 75, started at 2017-12-13T21:57:13Z and ended at 2017-12-14T22:10:56Z.
call_id: 76, started at 2017-12-12T15:07:58Z and ended at 2017-12-12T15:12:56Z.
call_id: 77, started at 2018-02-28T21:57:13Z and ended at 2018-03-01T22:10:56Z.
'''

import requests


class Sample:
    source = '99988526423'
    destination = '9933468278'

    def __init__(self, server):
        self._server = server

    def insert(self, call_id, start, end):
        self._make_request(call_id, 'start', start)
        self._make_request(call_id, 'end', end)

    def make_data(self, call_id, type, time):
        return {'type': type, 'time_stamp': time,
                'call_id': call_id, 'source': self.source, 'destination': self.destination}

    def _make_url(self):
        return self._server + 'phone_record/'

    def _make_request(self, call_id, type, time):
        my_request = requests.post(self._make_url(), self.make_data(call_id, type, time))
        print('{%d} (%s): %d `%s`' % (call_id, type, my_request.status_code, my_request.text))


if __name__ == '__main__':
    sample = Sample('http://127.0.0.1:8000/')

    sample.insert(70, '2016-02-29T12:00:00Z', '2016-02-29T14:00:00Z')
    sample.insert(71, '2017-12-11T15:07:13Z', '2017-12-11T15:14:56Z')
    sample.insert(72, '2017-12-12T22:47:56Z', '2017-12-12T22:50:56Z')
    sample.insert(73, '2017-12-12T21:57:13Z', '2017-12-12T22:10:56Z')
    sample.insert(74, '2017-12-12T04:57:13Z', '2017-12-12T06:10:56Z')
    sample.insert(75, '2017-12-13T21:57:13Z', '2017-12-14T22:10:56Z')
    sample.insert(76, '2017-12-12T15:07:58Z', '2017-12-12T15:12:56Z')
    sample.insert(77, '2018-02-28T21:57:13Z', '2018-03-01T22:10:56Z')
