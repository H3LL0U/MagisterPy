This library will help you interact with your magister account using python!

Disclaimer: it is against Magister's TOS to use anauthorized API's. Use at your own risk
https://magister.nl/over-ons/juridische-zaken/

Basic usage
```
session = MagisterSession()
session.login(school_name="School_name",username="username",password="your_password")
print(session.get_schedule("2024-11-03","2024-11-10"))
'''

More functionality to come!
