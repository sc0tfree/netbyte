from setuptools import setup
from netbyte import __version__ as VERSION

setup(
    name='netbyte',
    version=VERSION,
    url='http://www.sc0tfree.com',
    license='MIT License',
    author='sc0tfree',
    author_email='henry@sc0tfree.com',
    description='Netbyte is a Netcat-style tool that facilitates manual probing, fuzzing and exploitation of TCP and UDP services. It is lightweight, fully interactive and supports input and output in both plain text and hexadecimal.',
    keywords='fuzzing netcat utils cli hexadecimal',
    packages=['netbyte'],
    install_requires=[
        'colorama',
    ],
    entry_points = {
        "console_scripts" : ['netbyte = netbyte.__main__:main']
    },
)
