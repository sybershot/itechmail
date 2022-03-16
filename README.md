# Itechmail
Simple automated email sending task.

Steps:
1. Using (.json file) added to this task deserialize data from the file to object.
2. Using Mail API send an email from mail.ru service to yopmail as Recipients.TO and  mailto.plus as Recipients.CC.
3. Find the email using Selenium in yopmail service.
4. Parse email to object
5. Find the email using rest assured in mailto service
6. Parse mail to new object
7. Assert that all emails have correct data

Note: JSON file is located in `config` directory.

# Requirements

All requirements are listed in `requirements.txt` file.

# Prerequisites

Before launching the test, user must provide credentials for SMTP service. Path to the file must be specified
in `config/constants.py` by changing `MAIL_CREDENTIALS` variable and must have `.py` file extension.

Structure of the credentials file with example credentials:
```
MAIL_LOGIN = "John@smith.com"
MAIL_PASSWORD = "JohnSmith"
```

# Configuration

Configuration file is located in `config/constants.py`.
Available options:

- TIMEOUT – timeout for Selenium in seconds;
- BROWSER_TYPE – type of the driver for selenium;
- MESSAGE_PATH – path to the .JSON file containing message; 
- MAIL_CREDENTIALS – path to the mail credentials file;
- SMTP_SERVER – path to the SMTP server;
- SSL_PORT – port for the SMTP server.

Supported driver types:
- Chrome
- Chromium
- Edge
- Firefox
- Opera
- IE

If you already have downloaded desired driver you can specify driver path
in `utils/browser_manager/drivermanager_config.py` file.
# Usage

Test can be launched using the following command:
```commandline
python3 -m  robot.run -V config/constants.py project/tests/mail_test.robot
```