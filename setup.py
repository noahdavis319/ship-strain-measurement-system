
from setuptools import setup


config = {
    'name': 'ssms',
    'version': '0.1',
    'author': 'Noah Davis',
    'packages': ['ssms'],
    'package_dir': {'': 'src/main/python'},
    'author_email': 'noahdavis@gwu.edu',
    'description': 'Perform strain measurements using computer vision.',
    'entry_points': {
        'console_scripts': ['ssms=ssms.cli:cli']
    }
}

setup(**config)
