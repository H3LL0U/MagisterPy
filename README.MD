# MagisterPY

This library will help you interact with your magister account using python!

## Disclaimer: 
Please note: Using unauthorized APIs to access Magister is against Magister’s Terms of Service. 
By using this library, you assume all responsibility and accept any risks associated with breaching these terms. 
For more details, please refer to Magister's Terms of Service. (https://magister.nl/over-ons/juridische-zaken/)

## Installation
```
pip install git+https://github.com/H3LL0U/MagisterPy.git
```
or 
```
pip install MagisterPy
```

## Contributing
Feel free to create an issue if something doesn't work. It's only been tested on a singular school so far so it is to be expected. If you want to help add a feature it would be great as well! :D

## Basic usage
The following code snippet demonstrates how to create a session, log in, and retrieve your schedule and recent grades:
```
from magisterpy import MagisterSession

# Create a new session and log in
session = MagisterSession()
session.login(school_name="School_name", username="your_username", password="your_password")

# Get schedule for a specific date range
my_schedule = session.get_schedule("2024-11-03", "2024-11-10")

# Get the most recent grade
my_most_recent_grade = session.get_grades(top=1)[0]["waarde"]

print("Schedule:", my_schedule)
print("Most Recent Grade:", my_most_recent_grade)
```
With MagisterPy, you can access and manage your Magister account directly from Python, automating repetitive tasks and integrating your school data into your projects. We hope you find it helpful!
More functionality to come!
