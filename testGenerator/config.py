import os
from dotenv import load_dotenv

load_dotenv()



# Access the environment variables
GPT_MODEL_NAME = os.getenv('gpt_model_name')
MAX_TOKENS_COUNT = int(os.getenv('max_tokens_count', 2000))
TEMPERATURE = float(os.getenv('temperature', 0))
STREAMING = os.getenv('streaming', 'False')



