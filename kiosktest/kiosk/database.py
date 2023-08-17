from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import json

# 경로 지정 수정
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk')  # [YOUR_USERNAME]에 현재 사용자 이름을 입력하세요.
SECRET_FILE = r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk\secrets.json'  # [YOUR_USERNAME]에 현재 사용자 이름을 입력하세요.

with open(SECRET_FILE, 'r') as f:
    secrets = json.load(f)

DB = secrets['DB']

DB_URL = f"mysql+pymysql://{DB['USER']}:{DB['PASSWORD']}@{DB['HOST']}:{DB['PORT']}/{DB['NAME']}?charset=utf8"

engine = create_engine(
    DB_URL
)

SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False, 
                            bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        

