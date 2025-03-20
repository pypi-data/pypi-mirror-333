from setuptools import setup, find_packages
from os.path import join, dirname

import pynauriz

setup(
    name='pynauriz',
    version=pynauriz.__version__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    author='Naurizbek Aitbaev',
    author_email='nauriz.aitbai@gmail.com',
    description='Набор полезных инструментов и утилит для Python.',
    url='https://github.com/NaurizAitbai/pynauriz',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
