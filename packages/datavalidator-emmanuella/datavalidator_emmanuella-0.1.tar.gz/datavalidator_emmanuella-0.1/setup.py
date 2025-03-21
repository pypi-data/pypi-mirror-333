from setuptools import setup, find_packages

setup(
    name='datavalidator-emmanuella',
    version='0.1',
    packages=find_packages(exclude=["tests"]),  # Exclude the tests folder
    install_requires=[],  # No external dependencies
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple data validation package',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

