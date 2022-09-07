from peewee import *
from config.db import db_descriptor

db = SqliteDatabase(db_descriptor)

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.