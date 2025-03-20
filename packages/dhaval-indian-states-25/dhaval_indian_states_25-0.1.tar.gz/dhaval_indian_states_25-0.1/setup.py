from setuptools import setup,find_packages

setup (
    name="dhaval_indian_states_25",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Django'],
    license="MIT",
    description="A Django app that provides Indian States choices as a model and form field.",
    author="Dhaval",
    author_email="dhavalpatil1510@gmail.com",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)

