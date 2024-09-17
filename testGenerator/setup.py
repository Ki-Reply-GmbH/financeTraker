from llm_setup import setup_llm
from prompts import setup_test_generation_case_prompt, setup_test_generation_case_fewshot_prompt
from output_parser import CustomCodeOutputParser, CustomCodeOutputParserForFewShot
from langchain.chains import LLMChain

# Setup the LLM model
llm = setup_llm()

# Setup the prompt
prompt = setup_test_generation_case_fewshot_prompt()

# Setup the output parser
output_parser = CustomCodeOutputParserForFewShot()

# Create the LLMChain
chain = LLMChain(llm=llm, prompt=prompt, output_parser=output_parser)
















































































'''

import getpass
import os
import dotenv

api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    raise ValueError("OpenAI API key not found. Please check the environment variable.")

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate

from langchain_core.messages import SystemMessage

from langchain_core.prompts import HumanMessagePromptTemplate




chat = ChatOpenAI(
    
    model="gpt-4-turbo",
    api_key=api_key,
    max_tokens=2000,
    temperature=0,
    streaming=False
    )


prompt_template = """You are tasked with generating a clear and concise description of a function and corresponding unit tests. The procedure is given in the Description Phase and the Unit Test Generation Phase. Follow them sequentially:
 

 
###Unit Test Generation Phase:###
 
Based on the initial description, craft corresponding unit tests from the  Human Message.
Utilize pytest and mocker for data-driven testing.
Structure the tests with clear Given blocks to enhance test coverage and support robust system development.
Include unit test code and inline documentation explaining the test purpose and logic.
Use mocks to simulate external dependencies accurately.
 
###Important Instructions:###
 
In your response, follow the exact format shown in the example below.
Escape all special characters in the code (e.g., double quotes, single quotes, new lines) with a backslash.
Make sure to include the appropriate import statements for the function and its dependencies.
 
Example:
 
Example: 
{
    "function_description": "GENERATED DESCRIPTION HERE",
    "code": "GENERATED CODE HERE"
} 
 
sample User Input: input is defined in  Human Message.
 
 
sample LLM Response:
 
{
    "function_description": "This function registers a new user. It takes a single input `user` of type `UserCreate`, attempts to create the user, and returns a success message. If an error occurs, it logs the error and raises an HTTP 500 exception.",
    "code": "import pytest\\n\\nasync def test_register_user(mocker):\\n\\t# Given\\n\\tuser_create_instance = UserCreate(username=\\\"testuser\\\", password=\\\"testpassword\\\")\\n\\tmock_create_user = mocker.patch('path.to.create_user')\\n\\tmock_logger = mocker.patch('path.to.logger.error')\\n\\tmock_http_exception = mocker.patch('path.to.HTTPException')\\n\\n\\t# When\\n\\tresponse = await register_user(user_create_instance)\\n\\n\\t# Then\\n\\tmock_create_user.assert_called_once_with(user_create_instance)\\n\\tassert response == {\\\"message\\\": \\\"User registered successfully\\\"}\\n\\n\\t# When Exception Occurs\\n\\tmock_create_user.side_effect = Exception(\\\"Error\\\")\\n\\twith pytest.raises(HTTPException) as exc_info:\\n\\t\\tawait register_user(user_create_instance)\\n\\tmock_logger.assert_called_once()\\n\\tassert exc_info.value.status_code == 500\\n\\tassert exc_info.value.detail == \\\"Error registering user\\\""
}
 
 
"""
prompt = ChatPromptTemplate.from_messages(

    [

        SystemMessage(

            content=(

                prompt_template

            )

        ),

        HumanMessagePromptTemplate.from_template("{input}"),

    ]

)

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

'''