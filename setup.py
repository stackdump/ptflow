from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        requirements=f.read().splitlines()

setup(
    name="ptflow",
    version="0.1.0",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description="",
    license='MIT',
    keywords='ptflow pflow pnml petri-net petri petrinet statemachine statevector eventstore',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    long_description="""
    """,
    url="",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License"
    ],
)
