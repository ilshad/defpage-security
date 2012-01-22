from datetime import datetime
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import synonym
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import String
from sqlalchemy import DateTime
from zope.sqlalchemy import ZopeTransactionExtension
from defpage.security.util import make_hash
from defpage.security.util import check_hash
from defpage.security.util import random_string

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(Unicode)
    created = Column(DateTime)

    _password = Column('password', Unicode(), nullable=False)

    def __init__(self, email, password_hash):
        self.email = email
        self._password = password_hash
        self.created = datetime.utcnow()

    def _set_password(self, password):
        self._password = make_hash(password)

    def _get_password(self):
        return self._password

    password = synonym("_password", descriptor=property(_get_password, _set_password))

    def validate_password(self, password):
        return check_hash(password, self.password)

class PendingRegistration(Base):

    __tablename__ = "pending_registrations"

    code = Column(String, primary_key=True)
    email = Column(Unicode)
    password = Column(Unicode(), nullable=False)
    created = Column(DateTime)

    def __init__(self, email, password):
        self.code = self._create_code()
        self.email = email
        self.password = make_hash(password)
        self.created = datetime.utcnow()

    def _create_code(self):
        while 1:
            code = random_string(20)
            exists = DBSession().query(PendingRegistration).filter(PendingRegistration.code==code).first()
            if not exists:
                return code

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
