import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))  # NOQA
from MagisterPy import *


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



class TestPersonProfile(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "id": 999001,
            "externeId": "xyz789",
            "accountExterneId": "acc987654321",
            "voorletters": "J.D.",
            "roepnaam": "Jane",
            "tussenvoegsel": None,
            "achternaam": "Doe",
            "stamnummer": 654321,
            "rollenVanGebruiker": ["Leerling"],
            "links": {
                "self": {"href": "/api/leerlingen/999001"},
                "foto": {"href": "/api/leerlingen/999001/foto"}
            }
        }
        self.profile = PersonProfile(self.valid_data)

    def test_getters(self):
        self.assertEqual(self.profile.get_id(), 999001)
        self.assertEqual(self.profile.get_externe_id(), "xyz789")
        self.assertEqual(self.profile.get_account_external_id(), "acc987654321")
        self.assertEqual(self.profile.get_initials(), "J.D.")
        self.assertEqual(self.profile.get_first_name(), "Jane")
        self.assertIsNone(self.profile.get_infix())
        self.assertEqual(self.profile.get_last_name(), "Doe")
        self.assertEqual(self.profile.get_student_number(), 654321)
        self.assertEqual(self.profile.get_roles(), ["Leerling"])
        self.assertEqual(self.profile.get_all_links()["foto"]["href"], "/api/leerlingen/999001/foto")
        self.assertEqual(self.profile.get_specific_link("foto"), "/api/leerlingen/999001/foto")
        self.assertEqual(self.profile.get_photo_link(), "/api/leerlingen/999001/foto")

    def test_is_valid(self):
        self.assertTrue(self.profile.is_valid())

        # Test missing key
        invalid_data = self.valid_data.copy()
        del invalid_data["voorletters"]
        self.assertFalse(PersonProfile(invalid_data).is_valid())


class TestAccountProfile(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "id": 888222,
            "naam": "user12345",
            "emailadres": "user12345@schooldomain.test",
            "mobielTelefoonnummer": "0611223344",
            "softtokenStatus": "nietGekoppeld",
            "isEmailadresGeverifieerd": False,
            "moetEmailadresVerifieren": True,
            "uuId": "abcd1234-5678-9012-efgh-3456ijkl7890",
            "links": {
                "self": {"href": "/api/accounts/888222"},
                "leerling": {"href": "/api/leerlingen/999001"}
            }
        }
        self.profile = AccountProfile(self.valid_data)

    def test_getters(self):
        self.assertEqual(self.profile.get_id(), 888222)
        self.assertEqual(self.profile.get_username(), "user12345")
        self.assertEqual(self.profile.get_email(), "user12345@schooldomain.test")
        self.assertEqual(self.profile.get_mobile_number(), "0611223344")
        self.assertEqual(self.profile.get_softtoken_status(), "nietGekoppeld")
        self.assertFalse(self.profile.is_email_verified())
        self.assertTrue(self.profile.must_verify_email())
        self.assertEqual(self.profile.get_uuid(), "abcd1234-5678-9012-efgh-3456ijkl7890")
        self.assertEqual(self.profile.get_specific_link("leerling"), "/api/leerlingen/999001")

    def test_is_valid(self):
        self.assertTrue(self.profile.is_valid())

        # Missing field test
        invalid_data = self.valid_data.copy()
        del invalid_data["emailadres"]
        self.assertFalse(AccountProfile(invalid_data).is_valid())


if __name__ == "__main__":
    unittest.main()
