import getpass
import os
import dotenv

api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    raise ValueError("OpenAI API key not found. Please check the environment variable.")

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_core.messages import SystemMessage

from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import FewShotChatMessagePromptTemplate



chat = ChatOpenAI(
    
    model="gpt-4-turbo",
    api_key=api_key,
    max_tokens=2000,
    temperature=0,
    streaming=False
    )


prompt_template = """You are tasked with generating a clear and concise description of a function and corresponding unit tests. / 
                    The procedure is given in the *** Unit Test Generation Phase ***. Follow them sequentially: /
 

### Unit Test Generation Phase: ###
 
- Based on the initial description, craft corresponding unit tests from the  Human Message.
- Utilize pytest and mocker for data-driven testing.
- Structure the tests with clear Given blocks to enhance test coverage and support robust system development.
- Include unit test code and inline documentation explaining the test purpose and logic.
- Use mocks to simulate external dependencies accurately.
 
###Important Instructions:###
 
In your response, follow the exact format shown in the example below.
Escape all special characters in the code (e.g., double quotes, single quotes, new lines) with a backslash.
Make sure to include the appropriate import statements for the function and its dependencies.
 

 
"""
llm_response_examples = [
    {
        "commoncode": """ 
        
        import pytest
        from app.models.user import UserCreate
        from app.services.user_services import create_user
        from app.models.models import get_db
        from sqlalchemy.orm import Session

        @pytest.fixture
        def mock_db_session(mocker):
            session_mock = mocker.MagicMock(spec=Session)
            session_mock.add = mocker.MagicMock()
            session_mock.commit = mocker.MagicMock()
            session_mock.refresh = mocker.MagicMock()
            yield session_mock

        @pytest.fixture
        def mock_get_db(mock_db_session):
            with mocker.patch('app.models.models.get_db', return_value=mock_db_session) as mock:
                yield mock
                
        """,
        "test1" : """
        
        @pytest.mark.asyncio
            async def test_create_user_success(mock_get_db):
            
            user_data = UserCreate(name="John Doe", email="john.doe@example.com", password="securepassword123")
            expected_user = user_data.dict()

            
            result_user = create_user(user_data)

            
            mock_get_db().add.assert_called_once_with(expected_user)
            mock_get_db().commit.assert_called_once()
            mock_get_db().refresh.assert_called_once_with(expected_user)
            assert result_user == expected_user

        """,
        "test2" : """
        
        @pytest.mark.asyncio
        async def test_create_user_failure(mock_get_db):
            
            user_data = UserCreate(name="John Doe", email="john.doe@example.com", password="securepassword123")
            mock_get_db().add.side_effect = Exception("Database Error")

            
            with pytest.raises(Exception) as exc_info:
                create_user(user_data)
            assert str(exc_info.value) == "Database Error"
        
        """,
    },
    
    
]

example_prompt = prompt_template(
    input_variables=["Commoncode","Test1", "Test2"],
    template = "{Commoncode}\n{Test1}\n{Test2}\n"
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples= llm_response_examples,
    example_prompt= example_prompt
)

prompt = ChatPromptTemplate.from_messages(

    [

        SystemMessage(

            content=(

                prompt_template

            )

        ),
        few_shot_prompt,
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