#!/usr/bin/env python
from bottle import route, get, run, template, static_file
import json
import xdg.BaseDirectory

# { name: { idx, status } }
switches = {}

def save_status():
  path = xdg.BaseDirectory.save_data_path('catsite')
  with open(path + '/switches', 'w') as outfile:
    json.dump(switches, outfile)

@get('/status')
def get_status():
  return switches

def turn(status, id):
  if id is None:
    for id in switches.copy().keys():
      switches[id]['status'] = status
  elif id in switches:
    switches[id]['status'] = status

  save_status()
  return get_status()

@get('/on')
@get('/on/<id>')
def turn_on(id=None):
  return turn('on', id)

@get('/off')
@get('/off/<id>')
def turn_off(id=None):
  return turn('off', id)

@get('/rename/<id>/<new_id>')
def rename(id, new_id):
  switch = switches[id]
  del(switches[id])
  switches[new_id] = switch

  save_status()
  return get_status()

@route('/')
@route('/<filename:path>')
def serve_static(filename='index.html'):
  return static_file(filename, root='client')

def main():
  global switches

  # load most specific data path
  path = None
  for path in xdg.BaseDirectory.load_data_paths('catsite'):
    print('loading ' + path)
    try:
      with open(path + '/switches', 'r') as infile:
        switches = json.load(infile)
    except FileNotFoundError:
      pass

  if not switches:
    for idx in range(1, 4):
      switches[idx] = { 'idx': idx }

  print('switches', switches)

  for switch in switches.values():
    switch['status'] = 'unknown'

  run(host='0.0.0.0', port=8144)

main()
