from db import db

# The crypto payment type. Each user can have multiple crypto payment type
# 
class BitcoinPayModel(db.Model):
    __tablename__ = "bitcoin"

    # class variables
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wallet_address = db.Column(db.String(256))

    #merge (for sqlalchemy to link tables)
    user = db.relationship("UserModel")

    def __init__(self, user_id, wallet_address, wallet_password):

        self.user_id = user_id
        self.wallet_address = wallet_address

    def json(self):
        return {
                    "id" : self.id,
                    "wallet address" : self.wallet_address,
        }