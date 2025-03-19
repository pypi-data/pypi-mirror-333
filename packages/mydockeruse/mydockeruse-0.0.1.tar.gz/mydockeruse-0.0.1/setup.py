from setuptools import setup, find_packages

setup(
    name='mydockeruse',
    version='0.0.1',
    description='mydockeruse tool',
    author='du7ec',
    author_email='dutec6834@gmail.com',
    url='https://github.com/FarAway6834/mydockeruse',
    packages=find_packages(exclude=[]),
    install_requires=['mytoolset'],
    keywords=['mydockeruse', 'mydockeruse tool', 'mytoolset'],
    python_requires='>=3.4',
    package_data={},
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
)