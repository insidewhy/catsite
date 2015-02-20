import picamera
from io import BytesIO
from threading import Thread, BoundedSemaphore
from time import sleep
from datetime import datetime, timedelta

pic_lock = BoundedSemaphore()
pic_expires = None
pic_requests = 0 # requests for images since last picture
pic_thread = None
pic_data = None

# options
vertical_flip = horizontal_flip = False
pic_interval = 30 # in seconds

def init(_opts):
  global vertical_flip, horizontal_flip, pic_interval
  vertical_flip = _opts.vertical_flip
  horizontal_flip = _opts.horizontal_flip
  pic_interval = _opts.pic_interval

def take_picture():
  _start_picture_thread()
  with pic_lock:
    return [pic_data, pic_expires]

def _take_pictures():
  global pic_data, pic_thread, pic_requests, pic_expires

  while True:
    with picamera.PiCamera() as camera:
      camera.vflip = vertical_flip
      camera.hflip = horizontal_flip
      stream = BytesIO()
      camera.start_preview()
      sleep(2)
      camera.capture(stream, 'jpeg')
      with pic_lock:
        pic_requests = 0
        pic_data = stream.getvalue()
        pic_expires = datetime.now() + timedelta(0, pic_interval + 5)

    sleep(pic_interval)
    with pic_lock:
      if pic_requests == 0:
        pic_data = None
        pic_thread = None
        break

def _start_picture_thread():
  global pic_thread, pic_requests
  with pic_lock:
    if pic_thread:
      pic_requests += 1
    else:
      pic_requests = 1
      pic_thread = Thread(target=_take_pictures)
      pic_thread.daemon = True
      pic_thread.start()
