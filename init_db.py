from src.domain.db import init_db, get_session

init_db("sqlite:///cpos.db")
print("Database initialized successfully")
