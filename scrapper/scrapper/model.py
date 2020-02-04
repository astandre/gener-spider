from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

engine = db.create_engine('mysql+pymysql://root:@localhost/oerintegrationdb')

Base = declarative_base(engine)


class Triple(Base):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text, nullable=False)
    predicate = db.Column(db.Text, nullable=False)
    object = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    __tablename__ = 'triple'
    # __table_args__ = {'autoload': True}


class CleanTriple(Base):
    id = db.Column(db.Integer, primary_key=True)
    subject_uri = db.Column(db.Text, nullable=False)
    predicate = db.Column(db.Text, nullable=False)
    subject_id = db.Column(db.Text, nullable=False)
    object = db.Column(db.Text, nullable=False)
    __tablename__ = 'cleantriple'


def load_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session
