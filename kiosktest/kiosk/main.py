from fastapi import FastAPI 
from starlette.middleware.cors import CORSMiddleware
from domain.menu import menu_router
from domain.order import order_router
from domain.orderer import orderer_router
from domain.recommendation import menu_reco
from domain.face_detect import face_detect_router
from domain.order import order_state_router
from domain.admin_ import meun_check_router

#

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(menu_router.router)
app.include_router(order_router.router)
app.include_router(menu_reco.router)
app.include_router(face_detect_router.router)
app.include_router(order_state_router.router)
app.include_router(meun_check_router.router)
app.include_router(orderer_router.router)