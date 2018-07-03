from app import db

class faqs(db.Model):
    __table__ = db.Model.metadata.tables['faqs']

    def __str__(self):
        return self.__table__.name

    def __repr__(self):
        return self.__table__.name