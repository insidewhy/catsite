#!/usr/bin/env python
from bottle import route, run, template

status = { '1': 'unknown', '2': 'unknown', '3': 'unknown', '4': 'unknown'}

@route('/status')
def get_status():
  return status

@route('/on/<id>')
def turn_on(id):
  if id in status:
    status[id] = 'on'
  return get_status()

@route('/off/<id>')
def turn_off(id):
  if id in status:
    status[id] = 'off'
  return get_status()

@route('/on')
def turn_all_on():
  for id in status.copy().keys():
    status[id] = 'on'
  return get_status()

@route('/off')
def turn_all_off():
  for id in status.copy().keys():
    status[id] = 'off'
  return get_status()

def main():
  run(host='localhost', port=8144)

main()
