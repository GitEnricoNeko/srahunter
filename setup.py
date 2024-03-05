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
     'pandas>=2.0.2',
     'psutil>=5.7',
     'pyfiglet>=0.8',
     'requests==2.31.0',
     'tqdm==4.66.1'
    ],
    packages=['.scripts'],  # Explicitly specifying packages if find_packages() was missing subpackages
    entry_points={
        'console_scripts': [
            'srahunter=cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # Assuming your package is for Python 3
        'Programming Language :: Python :: 3.6',  # Specify other versions as necessary
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)
