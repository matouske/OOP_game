from setuptools import setup

__project__ = "OOPgame"
__version__ = "1.0.0"
__description__ = "My adventure-like game in object-oriented style based on Cluedo board game."
__packages__ = ["OOPgame"]
__author__ = "Eva"
__requires__ = ["random"]

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    requires = __requires__,
)
