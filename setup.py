import os

from distutils import log
from setuptools import setup

from pi import __version__


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy"
]

setup(
    name="pi",
    version=__version__,
    packages=["pi", "twisted.plugins"],
    package_data={"twisted" : ["plugins/pi_plugin.py"]},
    author="Julian Berman",
    author_email="Julian@GrayVines.com",
    classifiers=classifiers,
    description="The glue holding together my Pi web service",
    license="MIT",
    long_description=long_description,
    url="https://github.com/Julian/PiPy",
    install_requires=["klein", "pyopenssl", "treq", "twisted"],
    include_package_data=True,
    zip_safe=False,
)


try:
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))
except Exception, e:
    log.warn("*** Failed to update Twisted plugin cache. ***")
    log.warn(str(e))
