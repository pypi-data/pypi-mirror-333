from distutils.util import convert_path
from os import path

import setuptools

main_ns = {}
with open(convert_path('text_explainability/_version.py')) as ver_file:
    exec(ver_file.read(), main_ns)  # nosec

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup( # type: ignore
    name = 'text_explainability',
    version = main_ns['__version__'],
    description = 'Generic explainability architecture for text machine learning models',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Marcel Robeer',
    author_email = 'm.j.robeer@uu.nl',
    license = 'GNU LGPL v3',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    url = 'https://text-explainability.readthedocs.io/',
    packages = setuptools.find_packages(), # type : ignore
    include_package_data = True,
    install_requires = [
        'shap',
        'instancelib>=0.5.0',
        'genbase>=0.3.6',
        'scikit-learn>=1.0.2',
        'plotly>=5.4.0',
        'sentence-transformers',  # optional in future
        'scikit-learn-extra',  # optional in future
        'imodels>=1.2.7',
    ],
    extras_require = {
        'fast': ['fastcountvectorizer>=0.1.0'],  # currently not supported due to tokenization issues
        'dev': ['genbase-test-helpers>=0.1.1'],
    },
    python_requires = '>=3.8',
)
