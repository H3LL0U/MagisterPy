This library will help you interact with your magister account using python!

Disclaimer: it is against Magister's TOS to use anauthorized API's. Use at your own risk
https://magister.nl/over-ons/juridische-zaken/

Basic usage
'''
session = MagisterSession()
session.login(school_name="School_name",username="username",password="your_password")
my_schedule = session.get_schedule("2024-11-03","2024-11-10")
my_most_recent_grade = session.get_grades(top = 1)[0]["waarde"]
'''

More functionality to come!