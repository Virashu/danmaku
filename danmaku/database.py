from peewee import *

PATH = __file__.replace("\\", "/").rsplit("/", 1)[0]
# look for database file in the same folder, not folder of execution
db = SqliteDatabase(PATH + "/DataBase.db")


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


class Saved(BaseModel):
    object = CharField()
    object_position = CharField()
    level = IntegerField()


db.connect()


# db.create_tables([EnemyTypes])


"""
basic_enemy = EnemyTypes.create(name="basic enemy", texture_file="basic_enemy.png", texture_size_width=50,
                                texture_size_height=25, speed=30, shoot_v=1500, hp=250, dm=50, endurance=0.1)
basic_enemy.save()



strong_enemy = EnemyTypes.create(name="strong enemy", texture_file="strong_enemy.png", texture_size_width=60,
                                texture_size_height=35, speed=20,
                                shoot_v=1000, hp=250, dm=50, endurance=0.1)
strong_enemy.save()
"""


def get_enemy_type(name):
    a = EnemyTypes.get(EnemyTypes.name == name)
    return (
        a.texture_file,
        (a.texture_size_width, a.texture_size_height),
        a.speed,
        a.shoot_v,
        a.hp,
        a.dm,
        a.endurance,
    )
