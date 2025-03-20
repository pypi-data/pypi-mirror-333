# setup.py
from setuptools import setup, find_packages

setup(
    name='asciititle',
    version='0.1.0',
    author='devvyyxyz',
    author_email='info@devvyy.xyz',
    description='A library for generating ASCII art with custom fonts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/devvyyxyz/asciititle',  # Update if applicable
    packages=find_packages(),
    include_package_data=True,  # Include files specified in MANIFEST.in
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # or your chosen license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
