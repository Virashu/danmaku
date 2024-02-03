"""Peewee database models"""

from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    FloatField,
    BooleanField,
)
from danmaku.utils import resource_path

# look for database file in the same folder, not folder of execution
db = SqliteDatabase(resource_path("DataBase.db"))


# pylint: disable=missing-class-docstring


class BaseModel(Model):
    class Meta:
        database = db


class EnemyTypes(BaseModel):
    name = CharField(unique=True)
    texture_file = CharField()
    texture_size_width = IntegerField()
    texture_size_height = IntegerField()
    speed = IntegerField()
    shoot_v = IntegerField()
    hp = IntegerField()
    dm = IntegerField()
    endurance = FloatField()
    cost = IntegerField()


class BulletTypes(BaseModel):
    name = CharField(unique=True)
    enemy = BooleanField()
    texture_file = CharField()
    radius = IntegerField()
    speed = IntegerField()
    vx = IntegerField()
    vy = IntegerField()


class PlayerTypes(BaseModel):
    name = CharField(unique=True)
    texture_file = CharField()
    texture_size_width = IntegerField()
    texture_size_height = IntegerField()
    speed = IntegerField()
    shoot_v = IntegerField()
    hp = IntegerField()
    dm = IntegerField()
    endurance = FloatField()


class SavedObjects(BaseModel):
    object = CharField()
    object_type = CharField()
    object_position = CharField()
    object_hp = IntegerField()
    object_damage = IntegerField()


class SavedGame(BaseModel):
    level = IntegerField()
    score = IntegerField()
