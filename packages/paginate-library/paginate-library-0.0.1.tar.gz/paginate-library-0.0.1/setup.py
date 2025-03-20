from setuptools import setup

version = '0.0.1'

long_description ='''
This is a Python library for working with API requests. To paginate data
'''

setup(
    name='paginate-library',
    version=version,
    author='Rudolf Kovalevskiy',
    author_email='kovalevskiy2017@outlook.com',
    description='This is a Python library for working with API requests',
    long_description=long_description,
    license='MIT',
    packages=['paginate-library'],
    install_requires=[
        'fastapi',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)