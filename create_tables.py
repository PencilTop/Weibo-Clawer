from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from datetime import datetime
from uuid import uuid1

Base = declarative_base()
engine = create_engine('sqlite:///weibo-clawer.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing' : True}
    
    user_id = Column(String(64), primary_key=True, default=uuid1().hex)
    weibo_id = Column(String(30), nullable=False)
    screen_name = Column(String)
    description = Column(String)
    profile_url = Column(String)
    profile_image_url = Column(String)
    verified = Column(Boolean)
    follow_count = Column(Integer)
    followers_count = Column(Integer)
    gender = Column(String)
    urank = Column(Integer)
    
    updated_on = Column(DateTime(), default=datetime.now)
    
class WeiBoContent(Base):
     __tablename__ = 'weibo_contents'
     __table_args__ = {'extend_existing' : True}
     
     content_id = Column(String(64), primary_key=True, default=uuid1().hex)
     weibo_id =  Column(String(30), nullable=False)
     clawed_at = Column(DateTime(), default=datetime.now)
     created_at = Column(String)
     attitudes_count = Column(Integer)
     comments_count = Column(Integer)
     reposts_count = Column(Integer)
     scheme = Column(String)
     text = Column(String)

if __name__=='__main__':
    Base.metadata.create_all(bind=engine)   
    print("tables created successfully!")  


     
     
     
    
    
    
    
    
    
    
    
    
    
    
    