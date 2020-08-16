from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='pass_calculator',
    version='0.1.1',
    description='A common pass calculator for ULTRA and RADS',
    long_description='A common pass calculator for ULTRA and RADS',
    license="GPL v3",
    author='psas',
    author_email='oresat@pdx.edu',
    url="https://github.com/oresat/uniclogs-software",
    packages=['pass_calculator'],
    install_requires=['skyfield'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
