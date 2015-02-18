#!/usr/bin/env python
from bottle import route, get, post, run, template, static_file, response
import xdg.BaseDirectory
from subprocess import call
import picamera
from io import BytesIO
import json
import argparse
from threading import Thread, BoundedSemaphore
from time import sleep

PICTURE_INTERVAL = 60 # in seconds

# TODO: use classes instead of globals
switches = {} # { name: { idx, status } }
opts = None

pic_lock = BoundedSemaphore()
pic_requests = 0 # requests for images since last picture
pic_thread = None
pic_data = None

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

@route('/camera')
def camera():
  start_picture_thread()
  response.content_type = 'image/jpeg'
  while not pic_data:
    sleep(1)
  with pic_lock:
    return pic_data

def take_pictures():
  global pic_data, pic_thread, pic_requests

  while True:
    with picamera.PiCamera() as camera:
      camera.vflip = opts.vertical_flip
      camera.hflip = opts.horizontal_flip
      stream = BytesIO()
      camera.start_preview()
      sleep(2)
      camera.capture(stream, 'jpeg')
      with pic_lock:
        pic_requests = 0
        pic_data = stream.getvalue()

    sleep(PICTURE_INTERVAL)
    with pic_lock:
      if pic_requests == 0:
        pic_thread = None
        break

def start_picture_thread():
  global pic_thread, pic_requests
  with pic_lock:
    if pic_thread:
      pic_requests += 1
    else:
      pic_requests = 1
      pic_thread = Thread(target=take_pictures)
      pic_thread.daemon = True
      pic_thread.start()

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
