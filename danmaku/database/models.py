"""Peewee database models"""

from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    BooleanField,
    FloatField,
)
from danmaku.utils import resource_path

# look for database file in the same folder, not folder of execution
db = SqliteDatabase(resource_path("DataBase.db"))


# pylint: disable=missing-class-docstring,too-few-public-methods


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
    endurance = IntegerField()
    cost = IntegerField()


class BulletTypes(BaseModel):
    name = CharField(unique=True)
    enemy = BooleanField()
    texture_file = CharField()
    texture_size_width = IntegerField()
    texture_size_height = IntegerField()
    hitbox_radius = IntegerField()
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
    endurance = IntegerField()
    hitbox_radius = IntegerField()


class SavedObjects(BaseModel):
    object = CharField()
    object_type = CharField()
    object_position = CharField()
    object_hp = IntegerField()
    object_damage = IntegerField()


class SavedGame(BaseModel):
    level = IntegerField()
    score = IntegerField()
    power = IntegerField()
    bombs = IntegerField()
    time = FloatField()


class Settings(BaseModel):
    name = CharField(unique=True)
    display_name = CharField()
    type = CharField()
    possible_values = CharField()
    value = CharField()
