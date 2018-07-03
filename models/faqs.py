from app import db
from sqlalchemy.orm import relationship
#from .users import Users #not adding relationships now. Let's see how fucked up we can get.

class Faqs(db.Model):
    __table__ = db.Model.metadata.tables['faqs']
    #user = relationship('Users', primaryjoin='Faqs.user_id == User.id', backref='Faqs')#adding relationships among tables

    def __str__(self):
        return self.__table__.name

    def __repr__(self):
        return self.__table__.name