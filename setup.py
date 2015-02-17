from distutils.core import setup

setup(
    name='catsite',
    version='0.0.1',
    author='J. Pike',
    author_email='pip@chilon.net',
    scripts='bin/catsite.py',
    url='http://github.com/nuisanceofcats/catsite',
    license='LICENSE.txt',
    description='Website control for energenie radio control board.',
    long_description=open('README.txt').read(),
    install_requires=['catstalker >= 0.0.2', 'bottle >= 0.12.0', 'pyxdg >= 0.25'],
)
