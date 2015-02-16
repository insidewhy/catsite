#!/usr/bin/env python
from bottle import route, get, run, template, static_file

switches = { '1': 'unknown', '2': 'unknown', '3': 'unknown', '4': 'unknown'}

@get('/status')
def get_status():
  return switches

def turn(status, id):
  if id is None:
    for id in switches.copy().keys():
      switches[id] = status
  elif id in switches:
    switches[id] = status
  return get_status()

@get('/on')
@get('/on/<id>')
def turn_on(id=None):
  return turn('on', id)

@get('/off')
@get('/off/<id>')
def turn_off(id=None):
  return turn('off', id)

@route('/')
@route('/<filename:path>')
def serve_static(filename='index.html'):
  return static_file(filename, root='client')

def main():
  run(host='0.0.0.0', port=8144)

main()
