import json
import requests

import pook

pook.on()

# Register a POST mock
(pook.post('httpbin.org/post')
    .json({'foo': 'bar'})
    .type('json')
    .header('Client', 'requests')
    .reply(204)
    .headers({'server': 'pook'})
    .json({'body': 'FIRST'}))
# Register with same URL but diff BODY
(pook.post('httpbin.org/post')
    .json({'foo': 'ha'})
    .type('json')
    .header('Client', 'requests')
    .reply(204)
    .headers({'server': 'pook'})
    .json({'body': 'SECOND'}))

res = requests.post(
    'http://httpbin.org/post',
    data=json.dumps({'foo': 'bar'}),
    headers={'Client': 'requests', 'Content-Type': 'application/json'}
)
print(res.status_code)
print(res.headers)
print(res.content)

res = requests.post(
    'http://httpbin.org/post',
    data=json.dumps({'foo': 'ha'}),
    headers={'Client': 'requests', 'Content-Type': 'application/json'}
)
print(res.status_code)
print(res.headers)
print(res.content)

pook.off()
