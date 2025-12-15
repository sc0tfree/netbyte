from setuptools import setup

setup(
    name='netbyte',
    version='0.5',
    url='http://www.sc0tfree.com',
    license='MIT License',
    author='sc0tfree',
    author_email='henry@sc0tfree.com',
    description='Netbyte is a Netcat-style tool that facilitates probing proprietary TCP and UDP services. It is lightweight, fully interactive and provides formatted output in both hexadecimal and ASCII.',
    keywords='utils cli netcat hexadecimal',
    packages=['netbyte'],
    install_requires=[
        'colorama',
    ],
    extras_require={
        'test': ['pytest>=7'],
    },
    python_requires='>=3.9',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
    ],
    entry_points = {
        "console_scripts" : ['netbyte = netbyte.netbyte:main']
    },
)
