from typing import Union


class JsonResponseItem():
    '''
    Base class for all of the response Items
    Makes sure that all of the dunder methods and all other methods that were not assigned are being applied to the inner json
    '''

    def __init__(self, json: Union[list, dict]):
        self.json = json
    # Apply all other methods to the original json

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            return getattr(self.json, name)(*args, **kwargs)
        return wrapper

    def __getitem__(self, key):
        return self.json[key]

    def __setitem__(self, key, value):
        self.json[key] = value

    def __delitem__(self, key):
        del self.json[key]

    def __contains__(self, key):
        return key in self.json

    def __iter__(self):
        return iter(self.json)

    def __len__(self):
        return len(self.json)

    def __repr__(self):
        return f"{repr(self.json)}"


class Lesson(JsonResponseItem):
    '''
    A helper object that helps you interact with the retrieved lessons from the schedule.
    '''

    def __init__(self, json: dict, cancelled=False):
        '''
        Initializes a Lesson instance.

        Args:
            json (dict): The JSON data representing the lesson.
            cancelled (bool, optional): Indicates if the lesson is cancelled. Defaults to False.
        '''
        super().__init__(json=json)
        self.cancelled = cancelled  # Should be set by the get_schedule method

    def is_valid(self) -> bool:
        '''
        Checks if the lesson JSON contains all required keys.

        Returns:
            bool: True if all required keys are present, False otherwise.
        '''
        required_keys = {
            "Start", "Einde", "LesuurVan", "LesuurTotMet", "DuurtHeleDag",
            "Omschrijving", "Lokatie", "Status", "Type", "Subtype",
            "IsOnlineDeelname", "WeergaveType", "Inhoud", "Opmerking",
            "InfoType", "Aantekening", "Afgerond", "HerhaalStatus",
            "Herhaling", "Vakken", "Docenten", "Lokalen", "Groepen",
            "OpdrachtId", "HeeftBijlagen", "Bijlagen", "Id"
        }

        if not isinstance(self.json, dict):
            return False

        return not bool(required_keys - self.json.keys())

    def is_cancelled(self) -> bool:
        '''
        Checks if the lesson was marked as cancelled.

        Returns:
            bool: True if the lesson is cancelled, False otherwise.
        '''
        return self.cancelled

    def get_id(self) -> Union[None, int]:
        '''
        Retrieves the unique lesson ID.

        Returns:
            int: The ID of the lesson if available.
            None: If the ID is missing in the JSON.
        '''
        return self.json.get("Id")

    def get_location(self) -> Union[None, str]:
        '''
        Retrieves the location of the lesson.

        Returns:
            str: The location name if available.
            None: If the location is not found.
        '''
        return self.json.get("Lokatie")

    def get_start_time(self) -> Union[None, str]:
        '''
        Retrieves the lesson's start time.

        Returns:
            str: The start time if available.
            None: If the start time is missing.
        '''
        return self.json.get("Start")

    def get_end_time(self) -> Union[None, str]:
        '''
        Retrieves the lesson's end time.

        Returns:
            str: The end time if available.
            None: If the end time is missing.
        '''
        return self.json.get("Einde")

    def get_teacher_names(self) -> Union[None, list[dict]]:
        '''
        Retrieves the list of teachers associated with the lesson.

        Returns:
            list[dict]: A list of dictionaries containing teacher details.
            None: If no teachers are found.
        '''
        return self.json.get("Docenten")

    def get_locations(self) -> Union[None, list[str]]:
        '''
        Retrieves the names of all assigned locations.

        Returns:
            list[str]: A list of location names.
            None: If no valid locations exist.
        '''
        location_list = self.json.get("Lokalen")

        if not isinstance(location_list, list):
            return None

        return [location["Naam"] for location in location_list if "Naam" in location]

    def get_subject_names(self) -> Union[None, list[str]]:
        '''
        Retrieves the names of the subjects associated with the lesson.

        Returns:
            list[str]: A list of subject names.
            None: If no valid subjects exist.
        '''
        subject_list = self.json.get("Vakken")

        if not isinstance(subject_list, list):
            return None

        return [subject["Naam"] for subject in subject_list if "Naam" in subject]

    def get_description(self) -> Union[None, str]:
        '''
        Retrieves the description of the lesson.

        Returns:
            str: description string
            None: If no valid description exist.
        '''
        return self.json.get("Omschrijving")


class Grade(JsonResponseItem):
    '''
    A helper object that helps you interact with retrieved grade data.
    '''

    def __init__(self, json: Union[list, dict]):
        '''
        Initializes a Grade instance.

        Args:
            json (Union[list, dict]): The JSON data representing the grade.
        '''
        super().__init__(json)

    def is_valid(self) -> bool:
        '''
        Checks if the grade JSON contains all required keys.

        Returns:
            bool: True if all required keys are present, False otherwise.
        '''
        required_keys = {
            "kolomId", "omschrijving", "ingevoerdOp", "vak", "waarde",
            "weegfactor", "isVoldoende", "teltMee", "moetInhalen",
            "heeftVrijstelling", "behaaldOp", "links"
        }

        if not isinstance(self.json, dict):
            return False

        return not bool(required_keys - self.json.keys())

    def get_id(self) -> Union[None, int]:
        '''
        Retrieves the unique ID of the grade.

        Returns:
            int: The grade ID if available.
            None: If the ID is missing.
        '''
        return self.json.get("kolomId")

    def get_value(self) -> Union[None, str]:
        '''
        Retrieves the grade value.

        Returns:
            str: The grade as a string.
            None: If the value is missing.
        '''
        return self.json.get("waarde")

    def get_lesson_code(self) -> Union[None, str]:
        '''
        Retrieves the subject code associated with the grade.

        Returns:
            str: The subject code if available.
            None: If no valid subject code exists.
        '''
        grade_lesson_json = self.json.get("vak")

        if grade_lesson_json is not None:
            return grade_lesson_json.get("code")

        return None

    def get_lesson_name(self) -> Union[None, str]:
        '''
        Retrieves the subject name associated with the grade.

        Returns:
            str: The subject name if available.
            None: If no valid subject name exists.
        '''
        grade_lesson_json = self.json.get("vak")

        if grade_lesson_json is not None:
            return grade_lesson_json.get("omschrijving")

        return None

    def get_entered_time(self) -> Union[None, str]:
        '''
        Retrieves the time when the grade was entered.

        Returns:
            str: The timestamp of when the grade was recorded.
            None: If the timestamp is missing.
        '''
        return self.json.get("ingevoerdOp")

    def get_weighting_factor(self) -> Union[None, int]:
        '''
        Retrieves the weighting factor of the grade.

        Returns:
            int: The weighting factor if available.
            None: If the weighting factor is missing.
        '''
        return self.json.get("weegfactor")
