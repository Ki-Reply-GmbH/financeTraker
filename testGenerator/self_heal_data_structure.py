from pydantic import BaseModel
from typing import List
from enum import Enum


class statusEnum(Enum):
    DONE = "Done"
    FAILED = "Failed"   
    NOT_STARTED = "Not Started"
    
class GeneratedTestForFunction(BaseModel):
    test_function_key: str = ""
    test_function_code: str = ""
    test_function_generated_name: str = ""
    test_error: str = ""
    retry_count: int = 0
    status: statusEnum = statusEnum.DONE

class TestFunctionGenerator(BaseModel):
    function_name: str = ""
    function_code: str = ""  
    generated_tests: List[GeneratedTestForFunction] = []

