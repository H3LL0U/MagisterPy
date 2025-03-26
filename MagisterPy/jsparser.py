import json
from .magister_errors import *


class JsParser():
    def __init__(self):
        pass

    def rfind_nth_instance(self, string: str, substring, n, start_from=-1):

        if start_from == -1:
            start_from = None

        index = string.rfind(substring, 0, start_from)

        if index != -1 and n > 1:
            return self.rfind_nth_instance(string, substring, n-1, index)
        return index

    def get_authcode_from_js(self, js_content: str):
        try:
            line = 1131

            buffer = 200
            authcode = ""
            # It is the only (for now) a string that appears right after the authcode obfuscation at line 1132
            authcode_identifier = "].map((function(t)"

            end_column = js_content.find(authcode_identifier)+1
            # Gets the last part of the authcode obfuscation
            js_content = js_content[end_column-buffer:end_column]

            start_column = self.rfind_nth_instance(js_content, "[", 2)
            js_content = js_content[start_column:]

            start_list_index = None
            content_list = []  # stores the 2 lists containing info about the authcode

            # Find the first and the second list
            for idx, _char in enumerate(js_content):

                if _char == "[":
                    start_list_index = idx

                if _char == "]" and (not (start_list_index is None)):

                    content_list.append(json.loads(
                        js_content[start_list_index:idx+1]))

                if len(content_list) > 1:
                    break

            def convert_to_int(a): return int(a)

            random_char_list, index_list = content_list

            index_list = list(map(convert_to_int, index_list))

            for idx in index_list:
                authcode += str(random_char_list[idx])

            return authcode
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except Exception:
            raise AuthcodeError()
