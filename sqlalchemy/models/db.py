import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


"""
Ficheiro com o modelo da base de dados.  
"""

Base = declarative_base()

# Pasta onde está localizada a base de dados
basedir = os.path.abspath(os.path.dirname(__file__))

# Ligação à base de dados sqlite
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))


class Users(Base):
    # tabela users (utilizadores)
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    # role -> nivel de acesso do utilizador, 0 por omissao
    role = Column(Integer, default=0)
    email = Column(String(255), nullable=False, index=True, unique=True)
    site = Column(String(255), nullable=True)
    password = Column(String(500), nullable=False)
    last_login = Column(DateTime())
    last_logout = Column(DateTime())
    created = Column(DateTime, default=datetime.datetime.utcnow())
    posts = relationship('Posts', backref='author', lazy='dynamic')
    comments = relationship('Comments', backref='author', lazy='dynamic')

    def __repr__(self):
        """
        Representação de um utilizador.
        Utilizado quando se faz print do objecto.
        """
        return '<User {}>'.format(self.email)


class Posts(Base):
    # tabela posts
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, index=True, unique=True)
    title = Column(String(255))
    content = Column(String(5000))
    last_edited = Column(DateTime,
                         default=datetime.datetime.utcnow(),
                         onupdate=datetime.datetime.utcnow())
    created = Column(DateTime, default=datetime.datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.id'))
    comments = relationship('Comments', backref='post', lazy='dynamic')

    def __repr__(self):
        """
        Representação de um post.
        Utilizado quando se faz print do objecto.
        """
        return '<Post {}>'.format(self.url)


class Comments(Base):
    # tabela comments (comentários)
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String(2000))
    last_edited = Column(DateTime,
                         default=datetime.datetime.utcnow(),
                         onupdate=datetime.datetime.utcnow())
    created = Column(DateTime, default=datetime.datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __repr__(self):
        """
        Representação de um comentário.
        Utilizado quando se faz print do objecto."""
        return '<Comment {}>'.format(self.content)


# Inicia a base de dados
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
