#!/usr/bin/env python
from bottle import route, get, post, run, template, static_file
import json
import xdg.BaseDirectory
from subprocess import call

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

  arg = '-'
  if status == 'off':
    arg += 'o'
  if id is not None:
    arg += 's' + str(switches[id]['idx'])
  call(['sudo', 'catstalker.py', arg])

  save_status()
  return get_status()

@post('/on')
@post('/on/<id>')
def turn_on(id=None):
  return turn('on', id)

@post('/off')
@post('/off/<id>')
def turn_off(id=None):
  return turn('off', id)

@post('/rename/<id>/<new_id>')
def rename(id, new_id):
  switch = switches[id]
  if new_id not in switches and switch:
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

  # restore switch state from fs
  for path in xdg.BaseDirectory.load_data_paths('catsite'):
    print('loading', path)
    try:
      with open(path + '/switches', 'r') as infile:
        switches = json.load(infile)
    except FileNotFoundError:
      pass

  if not switches:
    for idx in range(1, 5):
      switches[str(idx)] = { 'idx': idx }

  print('switches', switches)

  for switch in switches.values():
    switch['status'] = 'unknown'

  run(host='0.0.0.0', port=8144)

main()
