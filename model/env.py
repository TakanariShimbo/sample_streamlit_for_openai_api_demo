import os

from dotenv import load_dotenv
load_dotenv()


DEFAULT_OPENAI_API_KEY = os.environ.get("DEFAULT_OPENAI_API_KEY", None)