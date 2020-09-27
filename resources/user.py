from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_claims)
from models.user import UserModel

#class to login users
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="password",   type=str,   required=True, help="password cannot be blank")
    parser.add_argument(name="email",      type=str,   required=True, help="email cannot be blank")

    @classmethod
    def post(cls):
        data = cls.parser.parse_args() # get data <1>
        user = UserModel.find_by_email(data.get("email"))  # find user by email <2>

        if user and user.password == data.get("password"): # check password <3>
            access_token = create_access_token(identity=user.id, fresh=True) # create access token <4>
            refresh_token = create_refresh_token(identity=user.id) # create refresh token <5>
            return {
                    "access_token" : access_token,
                    "refresh_token" : refresh_token
                    }, 200

        return {"message" : "Invalid Credentials"}, 401


#class to register user
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="firstname", type=str, required=False, help="firstname cannot be blank",case_sensitive=False)
    parser.add_argument(name="middlename", type=str, required=False, help="middlename cannot be blank",case_sensitive=False)
    parser.add_argument(name="lastname", type=str, required=False, help="lastname cannot be blank", case_sensitive=False)
    parser.add_argument(name="password", type=str, required=True, help="password cannot be blank")
    parser.add_argument(name="email", type=str, required=True, help="email cannot be blank")
    parser.add_argument(name="image", type=str, required=False, help="user image")
    parser.add_argument(name="phoneno", type=str, required=True, help="phone number cannot be blank")
    parser.add_argument(name="address", type=str, required=False, help="Home address of user",case_sensitive=False)
    parser.add_argument(name="admin", type=bool, default=False, required=False, help="phone number cannot be blank")
    parser.add_argument(name="country", type=str, default=False, required=True, help="user's country",case_sensitive=False)
    parser.add_argument(name="lga", type=str, default=False, required=True, help="user's lga",case_sensitive=False)
    parser.add_argument(name="state", type=str, default=False, required=True, help="user's state",case_sensitive=False) 

    def post(self):
        data = UserRegister.parser.parse_args()

        #check if data already exist
        if UserModel.find_by_email(email=data["email"]): return {"message" : f"email {data['email']} already exists."},400 # 400 is for bad request
        
        user = UserModel(**data)

        #insert
        try:
            user.save_to_db()
        except Exception as e:
            print(f"error is ----> {e}")
            return {"message" : "An error occured inserting the item"}, 500 #Internal server error

        return user.json(), 201


# class to list all user
class UserList(Resource):
    @jwt_required
    def get(self):     
        claim = get_jwt_claims()
        if not claim["is_admin"]: 
            return {"message" : "Admin priviledge required."}, 401

        users = UserModel.find_all()
        if users: return {"users" : [ user.json() for user in users]},201
        return {"message" : 'Item not found'}, 400


#class to create user and get user
class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name="firstname",  type=str,   required=False, help="firstname cannot be blank",case_sensitive=False)
    parser.add_argument(name="middlename", type=str,   required=False, help="middlename cannot be blank",case_sensitive=False)
    parser.add_argument(name="lastname",   type=str,   required=False, help="lastname cannot be blank", case_sensitive=False)
    parser.add_argument(name="password",   type=str,   required=False, help="password cannot be blank")
    parser.add_argument(name="email",      type=str,   required=True, help="email cannot be blank")
    parser.add_argument(name="image",      type=str,   required=False, help="user image")
    parser.add_argument(name="phoneno",    type=str,   required=True, help="phone number cannot be blank")
    parser.add_argument(name="address",    type=str,   required=False, help="Home address of user",case_sensitive=False)
    parser.add_argument(name="country",    type=str,   required=False, help="user's country",case_sensitive=False)
    parser.add_argument(name="lga",        type=str,   required=False, help="user's lga",case_sensitive=False)
    parser.add_argument(name="state",      type=str,   required=False, help="user's state",case_sensitive=False) 

    @classmethod
    @jwt_required
    def get(cls,userid=None):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid: 
            return {"message" : "Admin priviledge required."}, 401

        user = UserModel.find_by_id(id=userid)

        if user: return {"user" : user.json()},201
        return {"message" : 'user not found'}, 400

    #use for authentication before calling post
    @classmethod
    @jwt_required
    def put(cls,userid):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid: 
            return {"message" : "Admin priviledge required."}, 401

        data = User.parser.parse_args()
        user = UserModel.find_by_id(id=userid)
        email = UserModel.find_by_email(email=data["email"])
        
        if user:
            #update
            try:
                # for product in products: product.update_self_vars(data)
                if email and not (email.email == user.email): return {"message" : f"email {data['email']} already exists."},400 # 400 is for bad request
                for each in data.keys(): user.__setattr__(each, data[each])
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {"message" : "An error occured updating the item the item"}, 500 #Internal server error

        #confirm the unique key to be same with the product route
        else:
            user = UserModel(**data)
            try:
                if email: return {"message" : f"email {data['email']} already exists."},400 # 400 is for bad request
                user.save_to_db()
            except Exception as e:
                print(f"error is {e}")
                return {"message" : "An error occured inserting the item"}, 500 #Internal server error

        return user.json(), 201



    #use for authentication before calling post
    @classmethod
    @jwt_required
    def delete(cls,userid):
        claim = get_jwt_claims()
        if not claim["is_admin"] and claim["userid"] != userid: 
            return {"message" : "Admin priviledge required."}, 401
            
        user = UserModel.find_by_id(id=userid,)
        if user:
            user.delete_from_db()
            return {"message" : "User deleted"}, 200 # 200 ok 
            
        return {"message" : "User Not found"}, 400 # 400 is for bad request