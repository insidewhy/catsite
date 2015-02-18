from distutils.core import setup

setup(
    name='catsite',
    version='0.0.4',
    author='J. Pike',
    author_email='pip@chilon.net',
    scripts=['bin/catsite.py'],
    data_files=[('etc/sudoers.d', ['sudoers.d/catsite'])],
    url='http://github.com/nuisanceofcats/catsite',
    license='LICENSE.txt',
    description='Website control for energenie radio control board.',
    long_description=open('README.txt').read(),
    install_requires=['CatStalker >= 0.0.3', 'bottle >= 0.12.0', 'pyxdg >= 0.25', 'picamera >= 1.9'],
)
