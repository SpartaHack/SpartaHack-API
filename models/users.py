from app import db

class Users(db.Model):
    __table__ = db.Model.metadata.tables['users']

    def __str__(self):
        return self.__table__.name

    def __repr__(self):
        return self.__table__.name