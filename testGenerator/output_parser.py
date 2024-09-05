import json
from langchain_core.output_parsers import JsonOutputParser

class CustomCodeOutputParser(JsonOutputParser):
    def parse(self, text):
        print(f"Raw text to be parsed: {text}")  # Debug: Inspect raw text
        try:
            json_data = json.loads(text)  # Directly use json.loads to parse the string
            print(f"Parsed JSON data: {json_data}")  # Debug: Inspect parsed JSON
            code = json_data.get('code', 'No code key found in the response.')
            return code
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return "Parsing error"
        


class CustomCodeOutputParserForFewShot(JsonOutputParser):
    def parse(self, text):
        print(f"Raw text to be parsed: {text}")  # Debug: Inspect raw text
        try:
            json_data = json.loads(text)  # Directly use json.loads to parse the string
            print(f"Parsed JSON data: {json_data}")  # Debug: Inspect parsed JSON
            
            # Extract values for the specified keys
            common_code = json_data.get('commoncode', 'No "Common code" key found in the response.')
            test1 = json_data.get('test1', 'No "test1" key found in the response.')
            test2 = json_data.get('test2', 'No "test2" key found in the response.')

            # Return the extracted values as a dictionary
            full_code = {
                'commoncode': common_code,
                'test1': test1,
                'test2': test2
            }
            result = json.dumps(full_code)
            
            return result
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return "Parsing error"
