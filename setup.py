from setuptools import setup

VERSION = '1.0'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='Surge',
      version=VERSION,
      description='Surge Python SDK',
      author='Surge',
      author_email='team@surgehq.ai',
      url='https://github.com/surge-ai/surge-python',
      license="MIT",
      install_requires=requirements
     )
