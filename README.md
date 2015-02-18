![catsite](https://raw.github.com/nuisanceofcats/catsite/master/catsite.png)

A website written in python/polymer to let you control some household sockets via an [energenie pimote control](https://energenie4u.co.uk/index.phpcatalogue/product/ENER002-2PI) and view footage from a [raspberry pi camera](http://www.raspberrypi.org/products/camera-module/).

Ideal for deterring burglars and keeping an eye on your things while you're on holiday.

## Installation

Make sure python3, python3's pip and sudo are installed.

```shell
$ sudo pip install catsite
```

## Running

```shell
$ ./bin/catsite.py -h
usage: catsite.py [-h] [-v] [-H] [-p PORT]

raspberry pi home security/deterrence system

optional arguments:
  -h, --help            show this help message and exit
  -v, --vertical-flip   flip camera image vertically
  -H, --horizontal-flip
                        flip camera image horizontally
  -p PORT, --port PORT  port to run on
```

The default port is 8144. You must create a user called "catsite" to run this so that sudo will allow the user access to the GPIO pins (the pip package installs a file to /etc/sudoers.d).
