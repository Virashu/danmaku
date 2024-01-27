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


class BulletTypes(BaseModel):
    name = CharField(unique=True)
    texture_file = CharField()
    radius = IntegerField()
    vx = IntegerField()
    vy = IntegerField()


class SavedObjects(BaseModel):
    object = CharField()
    object_type = CharField()
    object_position = CharField()
    obj_damage = IntegerField()


class SavedGame(BaseModel):
    player_x = FloatField()
    player_y = FloatField()
    player_hp = FloatField()
    level = IntegerField()


#db.connect()
#db.create_tables([SavedGame])


"""
basic_enemy = EnemyTypes.create(name="basic enemy", texture_file="basic_enemy.png", texture_size_width=50,
                                texture_size_height=25, speed=30, shoot_v=1500, hp=250, dm=50, endurance=0.1)
basic_enemy.save()

strong_enemy = EnemyTypes.create(name="strong enemy", texture_file="strong_enemy.png", texture_size_width=60,
                                texture_size_height=35, speed=20,
                                shoot_v=1000, hp=250, dm=50, endurance=0.1)
strong_enemy.save()

boss = EnemyTypes.create(name="boss", texture_file="strong_enemy.png", texture_size_width=90,
                                texture_size_height=90, speed=10,
                                shoot_v=500, hp=550, dm=70, endurance=0.3)
boss.save()


basic_bullet = BulletTypes.create(name="basic enemy bullet", texture_file="bullet.png", radius=10, vx=0, vy=1)
basic_bullet.save()

basic_player_bullet = BulletTypes.create(name="basic player bullet", texture_file="bullet.png", radius=10, vx=0, vy=-1)
basic_player_bullet.save()
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


def get_bullet_type(name):
    a = BulletTypes.get(BulletTypes.name == name)
    return (
        a.texture_file,
        a.radius,
        (a.vx,
        a.vy)
    )


def get_saved_objects():
    objects = list()
    for el in SavedObjects.select():
        objects.append([el.object, el.object_type, (float(el.object_position.split(", ")[0]),
                        float(el.object_position.split(", ")[1])), el.obj_damage])
    return objects


def get_saved_game():
    for el in SavedGame.select():
        objects = [el.player_x, el.player_y, el.player_hp , el.level]
    return objects


def set_saved_objects(name, objects):
    for e in objects:
        n = SavedObjects.create(object=name, object_type=e.my_type,
                                object_position=str(e.x) + ", " + str(e.y), obj_damage=e.damage)
        n.save()


def set_saved_game(cur_level, player):
    n = SavedGame.create(player_x=player.x, player_y=player.y, player_hp = player.hp, level=cur_level)
    n.save()


def delete_saved_objects():
    for e in SavedObjects.select():
        SavedObjects.delete_by_id(e)
        SavedObjects.update()
    for e in SavedGame.select():
        SavedGame.delete_by_id(e)
        SavedGame.update()