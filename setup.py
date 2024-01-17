from setuptools import setup, find_packages

setup(
    name='SRAHunter',
    version='1.0.0', 
    author='Bortoletto Enrico',  
    author_email='enricobortoletto30@gmail.com',  
    description='A tool for processing SRA accessions',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/GitEnricoNeko/SRAHunter',  
    packages=find_packages(),  # Find all packages (directories with __init__.py)
    install_requires=[
        'pandas',  # List all your Python dependencies here
        'numpy',
        'psutil',
        'argparse'.
        'subprocess',
        'sys'
    ],
    entry_points={
        'console_scripts': [
            'srahunter=SRAHunter:main/scripts/SRA_download_and_dump_from_list.py',  # Replace with your script's function
        ],
    },
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Science/Research',
        'License :: MIT License' # Replace with your license
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.9',  # Replace with your Python version
)

