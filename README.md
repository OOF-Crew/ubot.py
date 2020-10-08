# ubot.py

Hi this is a little Telegram userbot I made in order to automatize various tasks that I find annoying to do otherwise.

## Installation
**Windows**
First you have to install [Python](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe).
Then open you `cmd` and type:

    pip install telethon pillow cryptg matplotlib logging
    git clone https://github.com/moresdavidewayan/ubot.py.git

**Arch Linux**
Open your terminal and run:

    sudo pacman -Syu pyhton python-pip
    sudo pip install telethon pillow cryptg matplotlib logging
    git clone https://github.com/moresdavidewayan/ubot.py.git
## Configure
When you run the file the program will ask if you want to use the values set in the configuration file(config.py). Using this method everytime you'll have to input your informations which 'll be annoying, so consider to change your information manually in the configuration file.
You'll need to connect to [Telegram](https://my.telegram.org) and generate your:
 1. API ID
 2. API hash 

Then you'll also need the name of your Telegram account.
The session name can be whatever you want

*If you change your session name the userbot 'll ask everytime your phone number and the code Telegram 'll send to you*
## How to run
Open your terminal in your working directory and type:

    python ubot.py
