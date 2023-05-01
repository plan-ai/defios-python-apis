import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="DefiOSPython",
    version="0.0.1",
    url="https://github.com/defi-os/defios-python-apis.git",
    license='MIT License',
    author="Tanmay Munjal",
    author_email="tanmaymunjal64@gmail.com",
    description="Python Flask API for defi-os",
    long_description=read("DefiOSPython/README.md"),
    packages=find_packages(exclude=('templates','tools',)),
    install_requires=required,
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)