from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()
