from db import db

class ModelsHelper:
    _childrelations = []
    def delete_from_db(self):
        self.delete_childrecords()
        db.session.delete(self)
        db.session.commit()
        
    def save_to_db(self):
        #connect to the database
        db.session.add(self)
        db.session.commit()

    def delete_childrecords(self):
        for each_relation in self._childrelations :
            for relation_details in self.__getattribute__(each_relation).all(): relation_details.delete_from_db()