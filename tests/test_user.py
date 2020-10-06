import unittest, json, os, requests

from app import *

# from db import db
URL = "http://127.0.0.1:5000/register"


class SignupTest(unittest.TestCase):
    def test_successful_signup(self):
        # Given
        data = {
            "firstname": "Gbenga",
            "middlename": "vincent",
            "lastname": "akinwande",
            "image": "path/to/images",
            "password": "1234",
            "phoneno": "0902517113333",
            "email": "gbengavincentakinwande22@gmail.com",
            "country": "Nigeria",
            "lga": "ondo west",
            "state": "ondo",
            "admin": False,
        }

        json_response = {
            "state": "ondo",
            "lga": "ondo west",
            "carts": [],
            "firstname": "Gbenga",
            "address": None,
            "lastname": "akinwande",
            "bitcoins": [],
            "country": "Nigeria",
            "admin": False,
            "email": "gbengavincentakinwande2@gmail.com",
            "middlename": "vincent",
            "cards": [],
            "image": "path/to/images",
            "id": 1,
            "created": "2020-10-01T21:21:16.112205",
            "phoneno": "090251711333",
            "stores": [],
            "favstores": [],
        }

        headers = {"Authorization": "Bearer "}

        response = requests.request("POST", URL, headers=headers, json=data)
        status_code = response.status_code
        response = response.json()

        # Then
        self.assertEqual(201, status_code), "status code not 201"
        # self.assertEqual(response, json_response), "Response json data not the same"

    def tearDown(self):
        db_ = str(app.config["SQLALCHEMY_DATABASE_URI"].split("///")[1])
        if os.path.exists(db_):
            os.remove(db_)
        db.create_all(app=app)
