import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
SUPERMEMORY_API_KEY = os.getenv('SUPERMEMORY_API_KEY', '')
DATABASE_PATH = os.getenv('DATABASE_PATH', '../data/app.db')
