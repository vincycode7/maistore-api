from db import db


# The bank payment type. Each user can have multiple bank payment type
#
class CardpayModel(db.Model):
    __tablename__ = "cardpay"
    # class variables
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    card_num = db.Column(db.String(256))
    card_cvv = db.Column(db.String(3))
    card_exp = db.Column(db.DateTime)

    # merge (for sqlalchemy to link tables)
    user = db.relationship("UserModel")

    def __init__(self, userid, card_num, card_cvv, card_exp):

        self.userid = userid
        self.card_num = card_num
        self.card_cvv = card_cvv
        self.card_exp = card_exp

    def json(self):
        return {
            "id": self.id,
            "card_num": self.card_num,
        }
