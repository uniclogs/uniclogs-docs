from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='pass_calculator',
    version='1.0',
    description='A common pass calculator for ULTRA and RADS',
    long_description='A common pass calculator for ULTRA and RADS',
    license="GPLv3",
    author='psas',
    author_email='oresat@pdx.edu',
    url="https://github.com/oresat/uniclogs-software",
    packages=['pass_calculator'],
    install_requires=['skyfield'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "OSI Approved :: GNU General Public License v3 (GPLv3)"
         "Operating System :: OS Independent",
     ],
)
