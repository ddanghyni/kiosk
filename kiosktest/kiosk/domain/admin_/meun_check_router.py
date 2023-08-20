import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk\domain\admin_')
from admin_schema import AdminOrderSummary
import sys
sys.path.append(r'C:\Users\user\Desktop\kiosk\kiosktest\kiosk')
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models
from typing import List


router = APIRouter(
    tags=['Admin']
)

@router.get("/admin/{customer_id}")
def admin_view(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.FaceAnalysis).filter(models.FaceAnalysis.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # orderer_id를 face_analysis_id로 변경
    orders = db.query(models.OrderDetail).filter(models.OrderDetail.face_analysis_id == customer_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")

    state = db.query(models.State).filter(models.State.id == customer_id).first()
    state_message = "매장" if state and state.state_name == 0 else "포장" if state and state.state_name == 1 else "Unknown"

    response = []
    total_price = 0
    total_menu_count = 0

    for order in orders:
        menu = db.query(models.Menu).filter(models.Menu.menu_pk == order.menu_pk).first()
        if not menu:
            continue

        options = db.query(models.Option_).filter(models.Option_.order_details.any(order_detail_pk=order.order_detail_pk)).all()
        options_list = [{"option_name": option.option_name, "option_price": option.option_price} for option in options]

        order_price = menu.menu_price + sum(option.option_price for option in options)

        order_summary = {
            "customer_name": customer.name,
            "menu_name": menu.menu_name,
            "menu_price": menu.menu_price,
            "options": options_list,
            "total_price": order_price
        }

        total_price += order_price
        total_menu_count += 1
        response.append(order_summary)

    return {
        "customer_name": customer.name,
        "orders": response,
        "total_menu_count": total_menu_count,
        "Final payment amount": total_price,
        "state": state_message  
    }


import io
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from collections import defaultdict
from matplotlib.ticker import MaxNLocator
import matplotlib.font_manager as fm
import matplotlib
matplotlib.use('Agg')

font_path = 'C:\\Users\\user\\Desktop\\NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path, size=10)

@router.get("/analysis/sales", response_class=StreamingResponse)
def analyze_sales(db: Session = Depends(get_db)):
    order_details = db.query(models.OrderDetail).all()

    menu_sales = defaultdict(int)
    gender_sales = defaultdict(int)
    age_sales = defaultdict(int)
    gender_menu_sales = defaultdict(lambda: defaultdict(int))
    age_group_menu_sales = defaultdict(lambda: defaultdict(int))

    for detail in order_details:
        menu = db.query(models.Menu).filter(models.Menu.menu_pk == detail.menu_pk).first()
        customer = db.query(models.FaceAnalysis).filter(models.FaceAnalysis.id == detail.face_analysis_id).first()

        menu_sales[menu.menu_name] += 1
        gender_sales[customer.gender] += 1
        age_group = f"{(customer.age // 10) * 10}s"
        age_sales[age_group] += 1
        gender_menu_sales[customer.gender][menu.menu_name] += 1
        age_group_menu_sales[age_group][menu.menu_name] += 1

    gender_top_menus = [max(menus.items(), key=lambda x: x[1])[0] for gender, menus in gender_menu_sales.items()]
    age_top_menus = [max(menus.items(), key=lambda x: x[1])[0] for age, menus in age_group_menu_sales.items()]

    plt.figure(figsize=(12, 8))

    # 메뉴별 판매량
    ax1 = plt.subplot(3, 1, 1)
    ax1.bar(menu_sales.keys(), menu_sales.values(), color='blue')
    ax1.set_title('Menu Sales', fontproperties=fontprop)
    ax1.set_xticks(range(len(menu_sales)))
    ax1.set_xticklabels(menu_sales.keys(), rotation=45, ha='right', fontproperties=fontprop)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    # 성별별로 가장 많이 팔린 메뉴
    ax2 = plt.subplot(3, 1, 2)
    ax2.bar(gender_sales.keys(), [gender_menu_sales[gender][menu] for gender, menu in zip(gender_sales, gender_top_menus)], color='green')
    ax2.set_title('Most Sold Menu by Gender', fontproperties=fontprop)
    ax2.set_xticks(range(len(gender_sales)))
    ax2.set_xticklabels([f"{gender} ({menu})" for gender, menu in zip(gender_sales, gender_top_menus)], rotation=45, ha='right', fontproperties=fontprop)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    # 연령대별로 가장 많이 팔린 메뉴
    ax3 = plt.subplot(3, 1, 3)
    ax3.bar(age_sales.keys(), [age_group_menu_sales[age][menu] for age, menu in zip(age_sales, age_top_menus)], color='red')
    ax3.set_title('Most Sold Menu by Age Group', fontproperties=fontprop)
    ax3.set_xticks(range(len(age_sales)))
    ax3.set_xticklabels([f"{age} ({menu})" for age, menu in zip(age_sales, age_top_menus)], rotation=45, ha='right', fontproperties=fontprop)
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    # Save to BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")