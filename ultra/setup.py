import setuptools
import ultra

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    dependencies = file.read().split('\n')[:-1]

setuptools.setup(
    name=ultra.APP_NAME,
    version=ultra.APP_VERSION,
    author=ultra.APP_AUTHOR,
    license=ultra.APP_LICENSE,
    description=ultra.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=ultra.APP_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    install_requires=dependencies,
    python_requires='>=3.8.5',
    entry_points={
        "console_scripts": [
            '{} = ultra.__main__:main'.format(ultra.APP_NAME),
        ]
    }
)
