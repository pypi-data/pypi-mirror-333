from setuptools import setup, find_packages 

setup(
    name='Data_Validator_Package',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Adenike Awotunde',
    author_email='adenikeisblessed@gmail.com',
    description='A simple personal data validation package',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Data-Epic/data-validator-Adenike-Awotunde",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.13.2'
)