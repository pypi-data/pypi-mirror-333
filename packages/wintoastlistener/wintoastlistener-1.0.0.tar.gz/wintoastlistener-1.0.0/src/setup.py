import sys
from distutils.core import setup

if sys.platform != "win32":
    raise RuntimeError("This package is only supported on Windows.")

setup(
    name='wintoastlistener',
    version='1.0.0',
    author='Gu-f',
    packages=['wintoastlistener'],
    scripts=[],
    url='https://github.com/Gu-f/WinToastListener',
    license='LICENSE',
    description='A python library implemented by python3, for listening to Toast message notifications on windows.',
    long_description=open('../README_EN.md', encoding="utf-8").read(),
    install_requires=[
        "pywin32 (>=308,==308.*)",
        "xmltodict (>=0.14.2,==0.14.2.*)",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ]
)
