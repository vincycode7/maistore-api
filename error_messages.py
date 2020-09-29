from marshmallow import ValidationError

BLANK_ERROR = "{} can not be left blank"
TO_INPUT = "input {}"
NOT_FOUND = "{} not found"
ADMIN_PRIVILEDGE_REQUIRED = "Admin priviledge required."
NOT_FOUND = "{} does not exist"
ERROR_WHILE_INSERTING = "An error occured inserting {}"
DELETED = "{} deleted"
INVALID_CREDENTIALS = "Invalid Credentials"
ALREADY_EXISTS = "{} {} already exists."
LODDED_OUT = "Successfully logged out."
def parser_or_err(schema, data):
    try:
        return schema.load(data), 200
    except ValidationError as err:
        return err.messages, 400