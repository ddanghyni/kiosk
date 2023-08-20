import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk\domain\order')
from order_schema import StateCreate
import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk')
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models
from typing import List




router = APIRouter(
    tags=['주문']
)



@router.post("/state/{id}")
def 매장or포장(id: int, state: StateCreate, db: Session = Depends(get_db)):
    new_state = models.State(state_name=state.state_name, id=id)
    db.add(new_state)
    db.commit()
    db.refresh(new_state)

    if new_state.state_name == 0:
        return {"message": "매장"}
    elif new_state.state_name == 1:
        return {"message": "포장"}
    else:
        raise HTTPException(status_code=400, detail="Invalid state_name value. It should be 0 or 1.")
