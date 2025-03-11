from MagisterPy import MagisterSession
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))


school_name = "your_school"
username = "your username"
password = "your password"


session = MagisterSession(
    automatically_handle_errors=True, enable_logging=False)


# You can also input your credentials seperately and check if they can be used (For example if you want to create a Client with seperate inputs)


input_school_response = session.input_school(school_name=school_name)

input_username_response = session.input_username(username=username)

input_password_response = session.input_password(password=password)

# Get schedule for a specific date range
my_schedule = session.get_schedule("2024-11-03", "2024-11-10")

# Get the most recent grade
my_most_recent_grade = session.get_grades(top=1)[0]["waarde"]

print("Schedule in json:", my_schedule)
print("Most Recent Grade:", my_most_recent_grade)
