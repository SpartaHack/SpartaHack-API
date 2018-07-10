from app import db
class Faqs(db.Model):
    __table__ = db.Model.metadata.tables['faqs']

    def __str__(self):
        return self.__table__.name

    def __repr__(self):
        return self.__table__.name