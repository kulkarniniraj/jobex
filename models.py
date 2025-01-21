from peewee import *

db = SqliteDatabase('people.db')

class SkillTag(Model):
    name = CharField()
    class Meta:
        database = db

class Person(Model):
    name = CharField()
    cv_location = CharField()
    experience = IntegerField()
    class Meta:
        database = db

class PersonSkill(Model):
    person = ForeignKeyField(Person, backref='skills')
    skill = ForeignKeyField(SkillTag, backref='persons')
    class Meta:
        database = db

class Position(Model):
    company = CharField()
    position_name = CharField()
    experience = IntegerField()
    class Meta:
        database = db

class PositionSkill(Model):
    position = ForeignKeyField(Position, backref='skills')
    skill = ForeignKeyField(SkillTag, backref='positions')
    class Meta:
        database = db

db.connect()
db.create_tables([SkillTag, Person, Position, PersonSkill, PositionSkill])
