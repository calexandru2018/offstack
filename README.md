<h1 align="center">Offstack App</h1>
<h3 align="center">Locally store <b>Stackoverflow</b> answers, comments, ratings and personal keywords of your favorite marked questions. <b>Only for Linux.</b></h3>

<div align="center">
    <a href="https://github.com/calexandru2018/offstack/releases/latest">
        <img alt="Build Status" src="https://img.shields.io/github/release/calexandru2018/offstack.svg?style=flat" />
    </a>
    <a href="https://github.com/calexandru2018/offstack/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/calexandru2018/offstack">
    </a>
    <a href="https://liberapay.com/calexandru2018/donate">
        <img src="http://img.shields.io/liberapay/goal/calexandru2018.svg?logo=liberapay">
    </a>
</div>
<div align="center">
    <a href="https://actions-badge.atrox.dev/calexandru2018/offstack/goto?ref=master">
        <img alt="Build Status" src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fcalexandru2018%2Foffstack%2Fbadge%3Fref%3Dmaster&style=flat" />
    </a>
    <a href="https://actions-badge.atrox.dev/calexandru2018/offstack/goto?ref=testing">
        <img alt="Build Status" src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fcalexandru2018%2Foffstack%2Fbadge%3Fref%3Dtesting&style=flat" />
    </a>    
</div>    

<br>
The idea with <b>Offstack</b> is to make sure that developpers have access to their favorite stackoverflow questions&answers locally their computer, without the need for opening the browser and searching for common known or previously searched issues.

### Installing Dependencies

**Dependencies:**

- python3.5+
- pip for python3 (pip3)
- setuptools for python3 (python3-setuptools)
- requests
- requests-oauthlib
- oauthlib
- selenium
- pyqt5
- <a href="https://github.com/mozilla/geckodriver/releases">geckodriver</a>


Install the following packages based on your distro:

| **Distro**                              | **Command**                                                                                                                           |
|:----------------------------------------|:---------------------------------------------------------------------------------------------------------                             |
|Fedora/CentOS/RHEL                       | `sudo dnf install -y python3-pip python3-setuptools python3-pyqt5`                                              |
|Ubuntu/Linux Mint/Debian and derivatives | `sudo apt install -y python3-pip python3-setuptools python3-pyqt5`                        |
|OpenSUSE/SLES                            | `sudo zypper in -y python3-pip python3-setuptools python3-pyqt5`  |
|Arch Linux/Manjaro                       | `sudo pacman -S python-pip python-setuptools python-pyqt5`       |


## Installing offstack

Before proceeding with with the next installation steps, make sure that you have downloaded <a href="https://github.com/mozilla/geckodriver/releases">geckodriver</a> and moved it into `/usr/lib` or `/usr/local/lib`, otherwise this will not work.

You can either install via <b>PIP</b> or by cloning the repository.

*Note: Make sure to run pip with sudo*

`sudo pip3 install offstack`

### To update to a new version

`sudo pip3 install offstack --upgrade`

## Manual Installation

1. Clone this repository

    `git clone https://github.com/calexandru2018/offstack`

2. Step into the directory

   `cd offstack`

3. Install

    `sudo python3 setup.py install`

### How to use

 `offstack`

### Not yet implemented:
- GUI
- Add own (personal) keywords
- Searching/Filter

## GUI Layout

<p align="center">
  <img src="https://i.imgur.com/hPYZw28.png" alt="Logo"></img>
</p>

<p align="center">
  <img src="https://i.imgur.com/nzWsIwn.png" alt="Logo"></img>
</p>
