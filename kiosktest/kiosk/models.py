from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

# 옵션 테이블
# 1. Option 모델 선언
class Option_(Base):
    __tablename__ = 'option_'
    __table_args__ = {'schema': 'kiosk'}
    option_pk = Column(Integer, primary_key=True, autoincrement=True)
    option_name = Column(String(50), nullable=False)
    option_price = Column(Integer, nullable=False)

#!2. order_option 연결 테이블 선언
order_option = Table(
    'order_option', Base.metadata,
    Column('order_detail_pk', Integer, ForeignKey('kiosk.order_detail.order_detail_pk')),
    Column('option_pk', Integer, ForeignKey('kiosk.option_.option_pk')))


# 카테고리 목록 테이블
class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'kiosk'}
    category_pk = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(50), nullable=False)
    

# 메뉴 테이블
class Menu(Base):
    __tablename__ = 'menu'
    __table_args__ = {'schema': 'kiosk'}
    menu_pk = Column(Integer, primary_key=True, autoincrement=True)
    menu_name = Column(String(50), nullable=False)
    menu_price = Column(Integer, nullable=False)
    menu_description = Column(String(50), nullable=False)
    category_pk = Column(Integer, ForeignKey('kiosk.categories.category_pk'))
    category = relationship('Categories', backref='menu')


#주문자 정보 테이블
# class Orderer(Base):
#     __tablename__ = 'orderer'
#     __table_args__ = {'schema': 'kiosk'}
#     orderer_id = Column(Integer, primary_key=True, index = True)
#     orderer_name = Column(String(50), nullable=False)
#     orderer_phone = Column(String(50), nullable=False)
#     orderer_gender = Column(String(10), nullable=False)
#     orderer_age = Column(Integer, nullable=False)


class FaceAnalysis(Base):
    __tablename__ = "face_analysis"
    __table_args__ = {'schema': 'kiosk'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), index=True)
    emotion = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)   


class OrderDetail(Base):
    __tablename__ = 'order_detail'
    __table_args__ = {'schema': 'kiosk'}
    
    order_detail_pk = Column(Integer, primary_key=True, autoincrement=True)
    face_analysis_id = Column(Integer, ForeignKey('kiosk.face_analysis.id'))  # 이름 변경 및 참조 수정
    menu_pk = Column(Integer, ForeignKey('kiosk.menu.menu_pk'))
    
    # options 관계 선언
    options = relationship('Option_', secondary=order_option, backref='order_details')
 

#! 메뉴 추천을 담당하는 모델

class RecommendedMenu(Base):
    __tablename__ = 'recommended_menu'
    __table_args__ = {'schema': 'kiosk'}
    rec_menu_pk = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    menu_pk = Column(Integer, ForeignKey('kiosk.menu.menu_pk'))
    menu = relationship('Menu', backref='recommended_menus')



class State(Base):
    __tablename__ = 'state'
    __table_args__ = {'schema': 'kiosk'}
    state_pk = Column(Integer, primary_key=True, autoincrement=True)
    state_name = Column(Integer, nullable=False) # 0 = 매장 , 1 = 포장
    id = Column(Integer, ForeignKey('kiosk.face_analysis.id'))
    face_analysis = relationship('FaceAnalysis', backref='state')
    







    
