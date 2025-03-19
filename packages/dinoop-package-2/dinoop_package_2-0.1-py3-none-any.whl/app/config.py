import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://d264adea82ff568031b10bcf:b102edb5a257bd78cacf3704@d11.fyre.ibm.com:5432/appdb")
