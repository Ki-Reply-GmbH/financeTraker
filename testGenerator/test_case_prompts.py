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



prompt_template = """

In the ***Human Message*** , You are given a file containing multiple Python unit test codes along with  \
their necessary imports and  modules. Your task is to generate unit test cases for each of these functions. \
Follow these instructions precisely:

  1. "Read the file" - The file contains various Python test codes with their corresponding imports and modules. 
  
  2. "Generate Unit Test Cases" -
      
    a. For each function in test codes, generate appropriate ***unit test cases***. ***your max limit is 4***  \
         for each of the functions.
         
    b. Ensure that the tests cover common use cases, edge cases, and any potential exceptions or errors.
 
  3. "Testing Framework" -
    
    a. You may use either the ***unittest*** or ***pytest*** framework to write the unit test cases.
    
    b. Ensure that the generated test file includes the necessary ***imports*** for the chosen framework.
    
The test cases should be clear, concise, and well-documented.

"""

chat = ChatOpenAI(
    
    model="gpt-4-turbo",
    api_key=api_key,
    max_tokens=2000,
    temperature=0.2,
    streaming=False
    )

prompt = ChatPromptTemplate.from_messages(

    [

        SystemMessage(

            content=(

                prompt_template

            )

        ),

        HumanMessagePromptTemplate.from_template("{test_codes_input}"),

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