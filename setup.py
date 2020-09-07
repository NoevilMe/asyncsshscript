import setuptools
from os import path

base_dir = path.abspath(path.dirname(__file__))

with open(path.join(base_dir, 'README.md')) as desc:
    long_description = desc.read()

with open(path.join(base_dir, 'asyncsshscript', 'version.py')) as version:
    exec(version.read())

setuptools.setup(
    name="asyncsshscript",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license='Eclipse Public License v2.0',
    description="running remote commands or scripts with asyncssh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms='Any',
    python_requires='>= 3.6',
    packages=setuptools.find_packages(),
    install_requires=['asyncssh >= 2.2.0'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ])
