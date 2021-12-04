# Hello Buddy!



* [Description](#description)
* [Features](#features)
* [Setup](#setup)

## Description:
A lazy script for lazy hackers to control their whole windows system using just voice commands and hand gestures without touching the keyboard and mouse. 

## Features:

All the listed below features can be done through just voice commands.

* **Play Music.**
* **Log Off/Turn off/Restart or put their computer on sleep.**
* **Open/close the task manager in case your system is frozen.**
* **Delete Temp Files if you think your system needs some extra space.**
* **Close all Processes.**
* **Activate/Deactivate virtual windows keyboard.** 
* **Activate Virtual mouse to turn on the camera and use mouse pointer from hand gestures.**

## Setup:

> [Create Google Cloud Account.](https://cloud.google.com/apigee/docs/hybrid/v1.5/precog-gcpaccount)

> Enable Cloud Speech-to-Text API.

> [Setup Authentication and Download key json file in current directory.](https://cloud.google.com/docs/authentication/getting-started)

> Rename key json file to "credentials.json"

>Rename .env.sample to .env

## Only for Windows:
1. Install chocolatey from [here](https://chocolatey.org/install) or run the below command on powershell.
```
$ Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
2. Then Install choco
```
$ choco install make
```
3. Clone the repository:
```
$ git clone https://github.com/Praveendwivedi/hello-buddy 
$ cd hello-buddy
$ make
```
  - for Windows:
  ```
    $ Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
    $ . venv\Scripts\activate
  ```
  - for linux:
  ```
  . ./venv/bin/activate
  ```
  - finally:
  ```
  $ make run
  ```  

# [Checkout this video](https://youtu.be/dxbS4dD5-d8)!!
