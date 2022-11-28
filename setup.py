from setuptools import setup, find_packages

VERSION = '1.0.28'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='surge-api',
      version=VERSION,
      description='Surge Python SDK',
      author='Surge',
      author_email='team@surgehq.ai',
      url='https://github.com/surge-ai/surge-python',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires='>=3.6',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=requirements,
      tests_require=['pytest >= 6.0.0'])
