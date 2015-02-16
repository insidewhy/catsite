#!/usr/bin/env python
from bottle import route, run, template

status = { '1': 'unknown', '2': 'unknown', '3': 'unknown', '4': 'unknown'}

@route('/status')
def get_status():
  return status

@route('/on')
@route('/on/<id>')
def turn_on(id=None):
  if id is None:
    for id in status.copy().keys():
      status[id] = 'on'
  elif id in status:
    status[id] = 'on'
  return get_status()

@route('/off')
@route('/off/<id>')
def turn_off(id=None):
  if id is None:
    for id in status.copy().keys():
      status[id] = 'on'
  elif id in status:
    status[id] = 'off'
  return get_status()

def main():
  run(host='localhost', port=8144)

main()
