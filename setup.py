import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'trunkver',
    version = '0.1.0-1-init-repo',
    author = 'Tarik Porto',
    author_email = 'tariklemos1511@gmail.com',
    license = 'GNU GPLv3',
    description = 'Calculates current repository version for trunk-based git strategy',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/tarikporto/trunkver',
    py_modules = ['trunkver', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        trunkver=trunkver:cli
    '''
)
