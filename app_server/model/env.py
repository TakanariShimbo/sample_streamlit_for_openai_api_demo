import os

from dotenv import load_dotenv
load_dotenv()


DEFAULT_OPENAI_API_KEY = os.environ["DEFAULT_OPENAI_API_KEY"]
DATABASE_TYPE = os.environ["DATABASE_TYPE"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = os.environ["DATABASE_PORT"]
DATABASE_DB = os.environ["DATABASE_DB"]
