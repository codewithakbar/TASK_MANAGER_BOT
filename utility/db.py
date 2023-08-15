from sqlalchemy import DateTime, ForeignKey, create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship




Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    chat_id = Column(Integer)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(String)
    lavozim = Column(String)
    phone = Column(String)

    personal = relationship("Personal", back_populates="user")


    # profile = relationship("UserProfile", uselist=False, back_populates="user")


class Personal(Base):
    __tablename__ = 'personal'

    id = Column(Integer, Sequence('personal_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_chat_id = Column(Integer, ForeignKey('users.chat_id'))
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(String)
    lavozim = Column(String)  # Add this line
    phone = Column(String)


    user = relationship("User", back_populates="personal")


# class UserProfile(Base):
#     __tablename__ = 'user_profiles'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), unique=True)
#     bio = Column(String)
#     # lavozim
#     position = Column(String)

#     user = relationship("User", back_populates="profile")


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users_chat_id = Column(Integer, ForeignKey('personal.user_chat_id'))


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    due_date = Column(DateTime)




