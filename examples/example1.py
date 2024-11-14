import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from MagisterPy import MagisterSession

# Create a new session and log in
session = MagisterSession()
session.login(school_name="School_name", username="your_username", password="your_password")

# Get schedule for a specific date range
my_schedule = session.get_schedule("2024-11-03", "2024-11-10")

# Get the most recent grade
my_most_recent_grade = session.get_grades(top=1)[0]["waarde"]

print("Schedule in json:", my_schedule)
print("Most Recent Grade:", my_most_recent_grade)