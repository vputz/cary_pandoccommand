from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

long_description = """
A Cary command which runs pandoc on the attached markdown file, returning
docx, epub, html, and pdf versions.
"""

setup(
    name='cary_pandoccommand',
    version='1.0.0',
    description='cary command for the unix pandoc command',
    long_description=long_description,
    # url='https://github.com/vputz/cary',
    author='Victor Putz',
    author_email='vputz@nyx.net',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],

    keywords='email',

    packages=['cary_pandoccommand'],

    install_requires=['cary'],

    extras_require={},

)
