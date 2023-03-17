from sqlalchemy import String, Column, Integer


from database import Base

class Book(Base):
    __tablename__  = "book"
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String)
    book_author = Column(String)