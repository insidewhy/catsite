#!/usr/bin/env python
from bottle import route, get, post, run, template, static_file, response
import xdg.BaseDirectory
from subprocess import call
import picamera
from io import BytesIO
import json
from threading import Thread, BoundedSemaphore
from time import sleep

PICTURE_INTERVAL = 60 # in seconds

switches = {} # { name: { idx, status } }

pic_lock = BoundedSemaphore()
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
  response.content_type = 'image/jpeg'
  with pic_lock:
    return pic_data

def take_pictures():
  global pic_data

  while True:
    with picamera.PiCamera() as camera:
      stream = BytesIO()
      camera.start_preview()
      sleep(2)
      camera.capture(stream, 'jpeg')
      with pic_lock:
        pic_data = stream.getvalue()
    sleep(PICTURE_INTERVAL)

def start_picture_thread():
  global pic_thread
  with pic_lock:
    if not pic_thread:
      pic_thread = Thread(target=take_pictures)
      pic_thread.daemon = True
      pic_thread.start()

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
      switches['switch ' + str(idx)] = { 'idx': idx }

  print('switches', switches)

  for switch in switches.values():
    switch['status'] = 'unknown'

  start_picture_thread()
  run(host='0.0.0.0', port=8144)

main()
