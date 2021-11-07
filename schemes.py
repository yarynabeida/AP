from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()


class NoteSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    text = fields.Str()
    idTag = fields.Int()
    idOwner = fields.Int()


class NoteStatisticsSchema(Schema):
    id = fields.Int()
    time = fields.Str()
    userId = fields.Int()
    noteId = fields.Int()


class TagSchema(Schema):
    id = fields.Int()
    name = fields.Str()
