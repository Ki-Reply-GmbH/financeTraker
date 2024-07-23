prompt =

"""
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