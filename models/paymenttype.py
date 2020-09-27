from db import db

# Admin will set this -- so users can pick from this
# This is like so in case more payment system comes in future


class PaytypeModel(db.Model):
    __tablename__ = "paytype"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    desc = db.Column(db.String(30))

    def __init__(self, description):
        self.desc = description

    def json(self):
        return {
            "id": self.id,
            "desc": self.desc,
        }
