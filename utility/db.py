from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    due_date = Column(DateTime)


class Personnel(Base):
    __tablename__ = 'personnel'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name = Column(String)
    position = Column(String)


