import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))  # NOQA
from MagisterPy import MagisterSession, Lesson, Grade


class TestLesson(unittest.TestCase):
    def setUp(self):
        self.valid_json = {
            "Start": "08:00", "Einde": "09:00", "LesuurVan": 1, "LesuurTotMet": 1,
            "DuurtHeleDag": False, "Omschrijving": "Math", "Lokatie": "Room 101",
            "Status": "Scheduled", "Type": "Lecture", "Subtype": "Normal",
            "IsOnlineDeelname": False, "WeergaveType": "Standard", "Inhoud": "Algebra",
            "Opmerking": "Bring calculator", "InfoType": "General", "Aantekening": "",
            "Afgerond": False, "HerhaalStatus": "None", "Herhaling": "None", "Vakken": [{"Naam": "Math"}, {"Naam": "Physics"}],
            "Docenten": [{"Naam": "Dr. Smith"}], "Lokalen": [{"Naam": "Room 101"}], "Groepen": [], "OpdrachtId": None,
            "HeeftBijlagen": False, "Bijlagen": [], "Id": 100
        }
        self.lesson = Lesson(self.valid_json)

    def test_is_valid(self):
        self.assertTrue(self.lesson.is_valid())

    def test_get_location(self):
        self.assertEqual(self.lesson.get_location(), "Room 101")

    def test_is_cancelled(self):
        self.assertFalse(self.lesson.is_cancelled())

    def test_get_start_time(self):
        self.assertEqual(self.lesson.get_start_time(), "08:00")

    def test_get_end_time(self):
        self.assertEqual(self.lesson.get_end_time(), "09:00")

    def test_get_teacher_names(self):
        self.assertEqual(self.lesson.get_teacher_names(),
                         [{"Naam": "Dr. Smith"}])

    def test_get_locations(self):
        self.assertEqual(self.lesson.get_locations(), ["Room 101"])

    def test_get_subject_names(self):
        self.assertEqual(self.lesson.get_subject_names(), ["Math", "Physics"])

    def test_get_id(self):
        self.assertEqual(self.lesson.get_id(), 100)

    def test_get_description(self):
        self.assertEqual(self.lesson.get_description(), "Math")


class TestGrade(unittest.TestCase):
    def setUp(self):
        self.valid_json = {
            "kolomId": 1, "omschrijving": "Exam", "ingevoerdOp": "2024-04-02",
            "vak": {"code": "MATH101", "omschrijving": "Mathematics"}, "waarde": "A",
            "weegfactor": 2, "isVoldoende": True, "teltMee": True, "moetInhalen": False,
            "heeftVrijstelling": False, "behaaldOp": "2024-04-01", "links": []
        }
        self.grade = Grade(self.valid_json)

    def test_is_valid(self):
        self.assertTrue(self.grade.is_valid())

    def test_get_value(self):
        self.assertEqual(self.grade.get_value(), "A")

    def test_get_lesson_code(self):
        self.assertEqual(self.grade.get_lesson_code(), "MATH101")

    def test_get_lesson_name(self):
        self.assertEqual(self.grade.get_lesson_name(), "Mathematics")

    def test_get_entered_time(self):
        self.assertEqual(self.grade.get_entered_time(), "2024-04-02")

    def test_get_weighting_factor(self):
        self.assertEqual(self.grade.get_weighting_factor(), 2)

    def test_get_id(self):
        self.assertEqual(self.grade.get_id(), 1)


if __name__ == "__main__":
    unittest.main()
