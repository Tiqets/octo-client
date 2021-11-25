from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='OCTo-API-client',
    version='1.0.3',
    description='HTTP client for OCTo (Open Connection for Tourism) APIs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'tonalite>=1.7.1,<2',
        'requests>=2.20.0,<3',
    ],
    extras_require={
        'tests': [
            'isort==4.3.21',
            'flake8-isort==2.7.0',
            'flake8==3.7.9',
            'mypy==0.770',
            'pytest-cov==2.8.1',
            'pytest==5.3.1',
            'responses==0.10.7',
            'tox==3.14.2',
        ]
    },
)
