import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///teste.db3')
# engine = create_engine('postgresql://usr:pass@localhost:5432/sqlalchemy')
Base = declarative_base()
Column(Integer, Sequence('user_id_seq'), primary_key=True)
Session = sessionmaker(bind=engine)

session = Session()

class User(Base):
    __tablename__ = 'users'
    # id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='Id do Usuário', unique=True)
    user = Column(String(20), nullable=False, comment='Usuário', unique=True)
    fullname = Column(String(50), comment='Nome completo')
    password = Column(String(12), comment='Senha')

    def __repr__(self):
        return "<User(user='%s', fullname='%s', password='%s')>" % (
                                self.user, self.fullname, self.password)

print(User.__table__)

Base.metadata.create_all(engine)

ed_user = User(user='ed1', fullname='Ed Jones1', password='edspassword1')
session.add(ed_user)

print(ed_user.user)

session.commit()

print(ed_user.id)