#!/usr/bin/env python

import sys
sys.path.append('.') # to find libcatsite during testing

import libcatsite.camera
from bottle import route, get, post, run, template, static_file, response, abort
import xdg.BaseDirectory
from subprocess import call
import json
import argparse

# TODO: use classes instead of globals
switches = {} # { name: { idx, status } }
opts = None

def save_status():
  path = xdg.BaseDirectory.save_data_path('catsite')
  with open(path + '/switches', 'w') as outfile:
    json.dump(switches, outfile)

@get('/status')
def get_status():
  response.set_header('Cache-Control', 'private, max-age=0, no-cache')
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

@route('/camera')
def camera():
  [img, expires] = libcatsite.camera.take_picture()
  if not img:
    # client will re-request
    abort(503, 'no pic yet')

  response.set_header('Cache-Control', 'private, max-age=0, no-cache')
  response.content_type = 'image/jpeg'
  response.expires = expires
  return img

def main():
  global switches, opts

  parser = argparse.ArgumentParser(
    description='raspberry pi home security/deterrence system')
  parser.add_argument('-v', '--vertical-flip', action='store_true',
    help='flip camera image vertically')
  parser.add_argument('-H', '--horizontal-flip', action='store_true',
    help='flip camera image horizontally')
  parser.add_argument('-p', '--port', type=int, default=8144,
    help='port to run on')
  opts = parser.parse_args()
  libcatsite.camera.init(opts)

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
      switches['switch ' + str(idx)] = { 'idx': idx }

  print('switches', switches)

  for switch in switches.values():
    switch['status'] = 'unknown'

  run(host='0.0.0.0', port=opts.port)

main()
