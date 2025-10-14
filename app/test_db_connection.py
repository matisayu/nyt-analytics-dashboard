from app.db import engine
from sqlmodel import text
#import socket
#socket.gethostbyname("db.idvhajbaznzqwzbkdtbe.supabase.co")

with engine.connect() as conn:
    result = conn.execute(text("SELECT now();"))
    print("Connected! Server time:", list(result))
