import json

class JsParser():
    def __init__(self):
        pass
    def get_authcode_from_js(self,js_content:str):
        line = 1192
        column = 15476
        buffer = 200
        authcode = ""
        js_content = js_content.split("\n")[line][column:column+buffer]
        start_list_index = None
        content_list = [] #stores the 2 lists containing info about the authcode
        
        #Find the first and the second list
        for idx, _char in enumerate(js_content):
            
            if _char == "[":
                start_list_index = idx
                
            if _char == "]" and (not (start_list_index is None)):
                
                content_list.append(json.loads(js_content[start_list_index:idx+1]))
            
            if len(content_list)>1:
                break
        
        if len(content_list) == 2:
            convert_to_int = lambda a: int(a)

            random_char_list, index_list = content_list

            index_list = list(map(convert_to_int,index_list))

            
            for idx in index_list:
                authcode+= random_char_list[idx]
        if len(authcode) == 8:
            return authcode
        return None
                

        