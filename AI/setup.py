from setuptools import setup
from setuptools import find_packages

REQUIRED_PACKAGES = [
    'numpy',
    'pandas',
    'keras',
    'tensorflow>=1.14.0',
    'tqdm',
    'matplotlib',
]

setup(
    name='NeoGameAI',
    version='0.1.0',
    description='A package containing the backend for NeoGame',
    packages=find_packages(exclude=('tests')),
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
)