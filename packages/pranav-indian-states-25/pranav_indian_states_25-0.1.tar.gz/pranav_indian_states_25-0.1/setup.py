from setuptools import setup,find_packages

setup(
	name="pranav_indian_states_25",
	version="0.1",
	packages=find_packages(),
	include_package_data=True,
	install_requires=["django"],
	license="MIT",
	description="A Django app that provides Indian states choices as a model and form field.",
	author="Pranav",
	author_email="pranavgaikwadmt12@gmail.com",
	classifiers=[
		"Framework :: Django",
		"Programming Language :: Python :: 3",
	],
)
	
	
	






