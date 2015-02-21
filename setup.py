from distutils.core import setup
from os.path import isfile
from os import listdir

def recursive_include(prefix, dir):
  ret = []
  files = []
  for path in listdir(dir):
    abs_path = dir + '/' + path
    if isfile(abs_path):
      files.append(abs_path)
    else:
      ret += recursive_include(prefix + '/' + path, abs_path)
  if len(files) > 0:
    ret += [(prefix, files)]
  return ret

share_files = recursive_include('usr/share/catsite/client', 'client')

setup(
    name='catsite',
    version='0.0.5',
    author='J. Pike',
    author_email='pip@chilon.net',
    scripts=['bin/catsite.py'],
    packages=['libcatsite'],
    data_files=[('etc/sudoers.d', ['sudoers.d/catsite'])] + share_files,
    url='http://github.com/nuisanceofcats/catsite',
    license='LICENSE.txt',
    description='Raspberry pi home security/deterrence system.',
    long_description=open('README.txt').read(),
    install_requires=['CatStalker >= 0.0.3', 'bottle >= 0.12.0', 'pyxdg >= 0.25', 'picamera >= 1.9'],
)
