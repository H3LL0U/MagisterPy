import sys  # NOQA
import os  # NOQA
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))  # NOQA
from MagisterPy import MagisterSession  # NOQA

# Create a new session and log in using with ... as ...: structure
with MagisterSession() as session:
    session.login(school_name="School_name",
                  username="your_username", password="your_password")

    # Get schedule for a specific date range
    my_schedule = session.get_schedule("2024-11-03", "2024-11-10")

    # Get the most recent grade
    my_most_recent_grade = session.get_grades(top=1)[0].get_value()

    print("Schedule in json:", my_schedule)
    print("Most Recent Grade:", my_most_recent_grade)
