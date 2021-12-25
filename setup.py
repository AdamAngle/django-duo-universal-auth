import os
from setuptools import setup

NAME = 'django-duo-universal-auth'
CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

# Pull the long description from the README file
long_description_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'README.md')

with open(long_description_filename) as fd:
    long_description = fd.read()

setup(
    name='django-duo-universal-auth',
    version='0.1.0',
    description='A simple Django middleware for Duo Universal 2-factor authentication.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AdamAngle/django-duo-universal-auth',
    author='Adam Angle',
    author_email='contact@adamangle.com',
    license='BSD 3-clause',
    install_requires=['duo-universal'],
    classifiers=CLASSIFIERS,
    packages=['duo_universal_auth'],
    include_package_data=True,
)
