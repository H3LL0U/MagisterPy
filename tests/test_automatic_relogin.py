import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))  # NOQA
from MagisterPy import MagisterSession


school_name = "some_school"
username = "some_username"
password = "some_password"
# Create a new session and log in
session = MagisterSession(
    automatically_handle_errors=False, enable_logging=True, enable_automatic_relogin=True)

input_school_response = session.input_school(school_name=school_name)


input_username_response = session.input_username(username=username)


input_password_response = session.input_password(password=password)

# Get schedule for a specific date range
my_schedule = session.get_schedule("2024-11-03", "2024-11-10")

# Get the most recent grade
my_most_recent_grade = session.get_grades(top=1)[0]["waarde"]

print("Schedule in json:", my_schedule)
print("Most Recent Grade:", my_most_recent_grade)


# Simulate the session expiring
#
session.app_auth_token = "some_random_string"


# This should not cause an error
print(session.get_grades(top=1)[0]["waarde"])
