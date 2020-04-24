"""setup.py: setuptools control."""



from setuptools import setup
from my_repo.constants import VERSION

long_descr = """
Locally store your Stackoverflow favorites, without the need to constantly look them up. Works only on Linux machines.

For further information and a usage guide, please view the project page:

https://github.com/calexandru2018/my-repo
"""

setup(
    name="my-repo-calexandru2018",
    packages=["my_repo"],
    entry_points={
        "console_scripts": ["my-repo = my_repo.main:init"]     
    },
    include_package_data=True,
    version=VERSION,
    description="Create own (local) repository of StackOverflow favorites (only for Linux).",
    long_description=long_descr,
    author="calexandru2018",
    license="GPLv3",
    url="https://github.com/calexandru2018/my-repo",
    install_requires=[
        "requests",
        "requests-oauthlib",
        "oauthlib",
        "setuptools",
        "selenium",
        "pyqt5",
    ],
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
