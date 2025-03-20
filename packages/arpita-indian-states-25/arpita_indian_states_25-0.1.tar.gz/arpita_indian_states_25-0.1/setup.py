from setuptools import setup,find_packages

setup(
	name = "arpita_indian_states_25",
	version="0.1",
	packages=find_packages(),
	include_package_data = True,
	install_requires =["django"],
	license="MT",
	description="A Django app that provides Indian state choices as a model and form field.",
	author="Arpita Hatkar",
	author_email="arpitahatkar1415@gmail.com",
	classifiers=[
		"Framework :: Django",
		"Programming Language :: Python :: 3",
	]
)