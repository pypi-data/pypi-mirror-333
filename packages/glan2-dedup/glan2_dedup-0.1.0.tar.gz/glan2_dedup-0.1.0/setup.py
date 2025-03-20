from setuptools import setup, find_packages

setup(
    name='glan2_dedup',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'datasketch>=1.5.8',
    ],
    author='shh',
    description='A document deduplication tool using MinHash',
    python_requires='>=3.7',
)