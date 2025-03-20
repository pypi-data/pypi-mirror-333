# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mltraq',
 'mltraq.steps',
 'mltraq.storage',
 'mltraq.storage.serializers',
 'mltraq.utils']

package_data = \
{'': ['*']}

install_requires = \
['cloudpickle>=2.2.0',
 'joblib>=1.4.0',
 'pandas>=1.5.3',
 'pyarrow>=10.0.0',
 'requests>=2.32.3,<3.0.0',
 'sqlalchemy>=2.0.0',
 'tabulate>=0.9.0',
 'tqdm>=4.64.1']

entry_points = \
{'console_scripts': ['mltraq = mltraq.cli:main']}

setup_kwargs = {
    'name': 'mltraq',
    'version': '0.1.165',
    'description': 'Track and Collaborate on ML & AI Experiments.',
    'long_description': '<p align="center">\n<img width="75%" height="75%" src="https://mltraq.com/assets/img/logo-wide-black.svg" alt="MLtraq Logo">\n</p>\n\n<p align="center">\n<img src="https://www.mltraq.com/assets/img/badges/test.svg" alt="Test">\n<img src="https://www.mltraq.com/assets/img/badges/coverage.svg" alt="Coverage">\n<img src="https://www.mltraq.com/assets/img/badges/python.svg" alt="Python">\n<img src="https://www.mltraq.com/assets/img/badges/pypi.svg" alt="PyPi">\n<img src="https://www.mltraq.com/assets/img/badges/license.svg" alt="License">\n<img src="https://www.mltraq.com/assets/img/badges/code-style.svg" alt="Code style">\n</p>\n\n---\n\n<h1 align="center">\nTrack and Collaborate on ML & AI Experiments.\n</h1>\n\nThe open-source Python library for ML & AI developers to design, execute and share experiments.\nTrack anything, stream, reproduce, collaborate, and resume the computation state anywhere.\n\n---\n\n* **Documentation**: [https://www.mltraq.com](https://www.mltraq.com/)\n* **Source code**: [https://github.com/elehcimd/mltraq](https://github.com/elehcimd/mltraq) (License: [BSD 3-Clause](https://mltraq.com/license/))\n* **Discussions**: [Ask questions, share ideas, engage](https://github.com/elehcimd/mltraq/discussions)\n* **Funding**: You can [star](https://github.com/elehcimd/mltraq) the project on GitHub and [hire me](https://www.linkedin.com/in/dallachiesa/) to make your experiments run faster\n\n---\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mltraq.com/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0',
}


setup(**setup_kwargs)
