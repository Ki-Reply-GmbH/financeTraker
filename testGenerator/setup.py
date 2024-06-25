import getpass
import os
import dotenv

api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    raise ValueError("OpenAI API key not found. Please check the environment variable.")

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate




chat = ChatOpenAI(
    
    model="gpt-3.5-turbo-0125",
    api_key=api_key,
    max_tokens=2000,
    temperature=0.2,
    streaming=False
    )


prompt_template = """Code Description Assistant is now designed to operate in two distinct phases for each piece of function code it processes. First, it generates a concise description that highlights the function's main purpose, inputs (including variable types), execution process, and output. This description captures the essence of the function in a clear, formal tone.
 
In the second phase, based on the initial description, Code Description Assistant crafts corresponding unit tests. It utilizes pytest and mocker for data-driven testing, structuring tests with clear Given, When, and Then blocks. The goal is to enhance test coverage and support robust system development. It starts with unit test code and includes inline documentation to explain test purpose and logic, ensuring clarity. Mocks are used to simulate external dependencies accurately.
 
This bifurcated approach allows for a clear separation between understanding the function's functionality and verifying its correctness through unit testing.

IMPORtANT!!
In your response follow the exact format as shown in the example below
IF there are double quotes in the code, escape them with a backslash
IF there are single quotes in the code, escape them with a backslash
IF there are new lines in the code, escape them with a backslash
IF there are any other special characters in the code, escape them with a backslash

{{
    "function_description": "GENERATED DESCRIPTION HERE",
    "code": "GENERATED CODE HERE"
}}
IE: 
userInput:"async def register_user(user: UserCreate):
    try:
        create_user(user)
        return {"message": "User registered successfully"}
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error registering user")"

LLM respons 
'{{
    function_description: this function adds two numbers and returns a number
    code: "
def test_create_user(mocker):\n\tuser_create_instance = UserCreate(username="testuser", password="testpassword")\nmock_db = mocker.MagicMock()\nmocker.patch("services.user_services.get_db", return_value=mock_db)\nresult = create_user(user_create_instance)\nmock_db.add.assert_called_once_with()\nmock_db.commit.assert_called_once()\nmock_db.refresh.assert_called_once_with(result)}}'\n"""
    
prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    ("human", "{input}")
])


from langchain_core.output_parsers import JsonOutputParser
import json

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

    
outputParser = CustomCodeOutputParser()
llm = LLMChain(llm=chat, prompt=prompt,output_parser=outputParser)