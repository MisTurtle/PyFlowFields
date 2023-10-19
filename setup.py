from setuptools import setup, find_packages

with open("README.md") as f:
	readme = f.read()

with open("LICENSE") as f:
	auth = f.read()

setup(
	name='PyFlowFields',
	version='0.0.2',
	description='Simulate the reaction of particles in an ever evolving flow field',
	long_description=readme,
	author='MisterTurtle',
	url='https://github.com/MisTurtle',
	license=auth,
	packages=find_packages(exclude='tests')
)
