# Time punch device using Raspberry PI
An employee clock on/off RFID device with RFID tags

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Project Status](#project-status)
* [Sources](#sources)

<a name="general-info"></a>
## General info 
This is built ontop of my Clock_timestamp_2 project, except the employee can clock on and off by scanning their
RFID card at the RFID device. Additionally, a remote database is used so that the hours worked timetable can viewed from any computer. 
This project is only the RFID device portion.
<a name="technologies"></a>
## Technologies
Software
* Python 3.x
* MySQL
* Tkinter 8.x
* Amazon's AWS RDS

Hardware
* Raspberry pi (I used the pi zero W)
* Mifare RC522 RFID Reader/Writer Module
* 1602A LCD Module
* 13.56Mhz RFID cards/tags

1602A LCD and RC522 RFID modules - I will link the repository in the resources that I used to get those working.

<a name="setup"></a>
## Setup
### Hardware setup
1. Setup up your raspberry pi initially if you haven't already. I've linked what I used in the resources section below.
2. Go to the Freenove repository (linked below) and follow the tutorial PDF for module pinout wiring. Find the pages for 
RFID and LCD wiring.

### Software setup
1. Once you've wired the Pi, continue following the tutorial PDF to setup the softwares required for each module.
2. Clone this repository into your pi
3. The pi runs python 2.x by default so we need to change it to run python 3.x, firstly pip install python3. After python3 is 
installed, follow [this](https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux)
handy guide to switch python3.x as the default.
4. Run pipenv install to download the dependencies required.
5. Create a .env file in the root folder of the project and fill in your remote database information with the format:
    * db_host='Remote database host'
    * db_user='Your user' 
    * db_pass='Your password'
    * database='Your database name'
6. Run rfid_controller.py, the LCD should light up after 10 seconds and the message "READY TO SCAN" should be displayed
    * Note: If rfid_controller.py fails to run becomes of missing modules, use sudo install 'missing package' to install.
7. You will just need to attach RFID cards to employees and when that card is scanned, it will search through the database and 
retrieve that particular user.

<a name="features"></a>
## Features
* Simple clock on/off RFID device for employees, they simply need to tap their RFID card to clock on/off
* Together with the timetable application in my other repository, you can view the updated timetable in real time
<a name="project-status"></a>
## Project Status
This project is primarily for personal learning and as such, it is still in development and not applicable for all business types.


<a name="sources"></a>
## Sources 
https://docs.python.org/3/library/ - Standard Python reference and guides <br/>
https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2 - Setting up Raspberry Pi initially
https://github.com/Freenove/Freenove_RFID_Starter_Kit_for_Raspberry_Pi - Tutorial PDF for module pinout wiring.

