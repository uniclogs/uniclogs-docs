import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='cosi-runner',
    version='1.0',
    author='psas',
    license='GPLv3',
    description=('Cosmos-Satnogs Interface:',
                 'Daemon for fetching telemetry and TLEs'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/oresat/uniclogs-software',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
)
