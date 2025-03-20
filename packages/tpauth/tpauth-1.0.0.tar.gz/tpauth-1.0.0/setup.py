# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tpauth', 'tpauth.response']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.28.1,<0.29.0', 'pydantic>=2.10.6,<3.0.0']

setup_kwargs = {
    'name': 'tpauth',
    'version': '1.0.0',
    'description': 'Python library simplifies the process of authenticating accounts with TP Servers.',
    'long_description': '',
    'author': 'Duy Nguyen',
    'author_email': 'duynguyen02.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
