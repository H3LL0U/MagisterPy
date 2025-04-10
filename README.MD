# ![Image](https://github.com/user-attachments/assets/47bd3819-8d4e-4e3e-82e6-b63ee9b66c3b)

This library will help you interact with your Magister account using python!

## Disclaimer: 
Please note: Using unauthorized APIs to access Magister might be against Magister’s Terms of Service. 
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
Feel free to create an issue if something doesn't work. It's only been tested on at least 2 schools so far so it is to be expected. If you want to help add a feature it would be great as well! :D
Also please create an issue if you have any questions!
## Basic usage
The following code snippet demonstrates how to create a session, log in, and retrieve your schedule and recent grades:
```
from MagisterPy import MagisterSession  

# Create a new session and log in.
with MagisterSession() as session:
    session.login(school_name="School_name",
                  username="your_username", password="your_password")

    # Get schedule for a specific date range
    my_schedule = session.get_schedule("2024-11-03", "2024-11-10")

    # Get the most recent grade
    my_most_recent_grade = session.get_grades(top=1)[0].get_value()

    print("Schedule in json:", my_schedule)
    print("Most Recent Grade:", my_most_recent_grade)
```
With MagisterPy, you can access and manage your Magister account directly from Python, automating repetitive tasks and integrating your school data into your projects. We hope you find it helpful!
More functionality to come!
