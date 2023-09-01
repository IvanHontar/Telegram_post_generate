
import os
from dotenv import load_dotenv


load_dotenv()


OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEEPAI_TOKEN = os.environ.get('DEEPAI_TOKEN')