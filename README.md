
# MeetAlumni

MeetAlumni is a platform to let students connect with their senior.


## Requirements
You should have python 3.9 or higher, I recommend the latest stable version of python and use a virtualenv.

To install the latest version of python, check the website bellow: https://www.python.org/downloads/

To check python version, run the following command

```bash
  python --version
```

To install virtualenv with pip, run

```bash
  python -m pip install virtualenv
  virtualenv --version
```

Create a virtualenv and activate it

```bash
  virtualenv venv
```

For macOS or in Unix using bash
```bash
  source venv/bin/activate
```

For Windows
```bash
  venv\Scripts\activate
```
## Installation

Activate your virtualenv and run the command

```bash
  python -m pip -r install requirements.txt
```
    
Configure the .env file according to your environment. Set the SECRET_KEY and the database credential.

To migrate the database, run the command
```bash
  python manage.py migrate
```
## Run Locally

Start the server

```bash
  python manage.py runserver
```

