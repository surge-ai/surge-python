from setuptools import setup, find_packages

VERSION = '1.0'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='surge',
      version=VERSION,
      description='Surge Python SDK',
      author='Surge',
      author_email='team@surgehq.ai',
      url='https://github.com/surge-ai/surge-python',
      license="MIT",
      packages=find_packages(exclude=["tests", "tests.*"]),
      install_requires=requirements,
      tests_require=["pytest >= 6.0.0"])
