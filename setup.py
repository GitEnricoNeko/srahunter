#!/usr/bin/env python
from setuptools import setup

setup(
    name='srahunter',
    version='1.0.0', 
    author='Bortoletto Enrico',  
    author_email='enricobortoletto30@gmail.com',  
    description='A tool for processing SRA accessions',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/GitEnricoNeko/SRAHunter',  
    install_requires=[
        'pandas',
        'numpy',
        'psutil',
        'argparse',
        'pyfiglet'
    ],
    scripts=['scripts/srahunter-download'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
)

