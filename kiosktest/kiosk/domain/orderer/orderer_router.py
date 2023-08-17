import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk\domain\orderer')
from orderer_schema import Orderer_
import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk')
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models
from typing import List


router = APIRouter(
    tags=['고객 정보']
)


#! 고객 정보 조회
@router.get('/orderer')
def 고객_정보_조회(db: Session = Depends(get_db)):
    orderer = db.query(models.FaceAnalysis).all()
    return orderer


