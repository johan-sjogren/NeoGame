from setuptools import setup
from setuptools import find_packages

REQUIRED_PACKAGES = [
    'numpy==1.18.1',
    'pandas==0.25.3',
    'keras==2.2.4',
    'tensorflow==1.14.0',
    'tqdm==4.41.1',
    'matplotlib==3.1.2',
    'gym==0.18.0',
]

setup(
    name='NeoGameAI',
    version='0.1.0',
    description='A package containing the backend for NeoGame',
    packages=find_packages(exclude=('tests')),
    python_requires='>=3.7, <3.8',
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
)