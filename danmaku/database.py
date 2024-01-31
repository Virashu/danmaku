from peewee import SqliteDatabase, Model, CharField, IntegerField, FloatField
from danmaku.utils import resource_path

# look for database file in the same folder, not folder of execution
db = SqliteDatabase(resource_path("DataBase.db"))


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
    player_x = FloatField()
    player_y = FloatField()
    player_hp = FloatField()
    level = IntegerField()


#db.connect()
#db.drop_tables([EnemyTypes])
#db.create_tables([EnemyTypes])
"""

basic_enemy = EnemyTypes.create(name="basic enemy",
                                texture_file="basic_enemy_2.png;basic_enemy_1.png;"
                                             "basic_enemy_2.png;basic_enemy_3.png",
                                texture_size_width=50, texture_size_height=65,
                                speed=30, shoot_v=1500, hp=250, dm=50, endurance=0.1)
basic_enemy.save()

strong_enemy = EnemyTypes.create(name="strong enemy",
                                 texture_file="strong_enemy_2.png;strong_enemy_1.png;"
                                              "strong_enemy_2.png;strong_enemy_3.png",
                                 texture_size_width=50,
                                 texture_size_height=65, speed=20,
                                 shoot_v=1000, hp=250, dm=50, endurance=0.1)
strong_enemy.save()

boss = EnemyTypes.create(name="boss",
                         texture_file="strong_enemy_2.png;strong_enemy_1.png;"
                                      "strong_enemy_2.png;strong_enemy_3.png",
                         texture_size_width=60, texture_size_height=85, speed=10,
                         shoot_v=500, hp=550, dm=70, endurance=0.3)
boss.save()


basic_enemy_bullet = BulletTypes.create(name="basic enemy bullet", enemy=True, texture_file="bullet.png", radius=10,
                                        speed=150, vx=0, vy=1)
basic_enemy_bullet.save()

basic_player_bullet = BulletTypes.create(name="basic player bullet", enemy=False, texture_file="bullet.png", radius=10,
                                         speed=150, vx=0, vy=-1)
basic_player_bullet.save()

player = PlayerTypes.create(name="player",
                            texture_file="player_idle_left.png;player_left_1.png;player_left_2.png;player_left_3.png;"
                                         "player_idle_left.png;player_left_4.png;player_left_5.png;player_left_6.png;"
                                         "player_idle_right.png;player_right_1.png;player_right_2.png;"
                                         "player_right_3.png;player_idle_right.png;player_right_4.png;"
                                         "player_right_5.png;player_right_6.png;player_idle_up.png;player_up_1.png;"
                                         "player_up_2.png;player_up_3.png;player_idle_up.png;player_up_4.png;"
                                         "player_up_5.png;player_up_6.png;player_idle_down.png;player_down_1.png;"
                                         "player_down_2.png;player_down_3.png;player_idle_down.png;player_down_4.png;"
                                         "player_down_5.png;player_down_6.png;player_shoot_1.png;player_shoot_2.png;"
                                         "player_shoot_3.png;player_shoot_4.png;player_idle_right.png",
                                 texture_size_width=50, texture_size_height=50,
                                 speed=150, shoot_v=250, hp=1300, dm=500, endurance=1)
player.save()"""


def get_enemy_type(name):
    a = EnemyTypes.get(EnemyTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "texture_size": (a.texture_size_width, a.texture_size_height),
        "speed": a.speed,
        "shoot_v": a.shoot_v,
        "hp":  a.hp,
        "dm": a.dm,
        "endurance": a.endurance,
    }


def get_player_type(name):
    a = PlayerTypes.get(PlayerTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "texture_size": (a.texture_size_width, a.texture_size_height),
        "speed": a.speed,
        "shoot_v": a.shoot_v,
        "hp":  a.hp,
        "dm": a.dm,
        "endurance": a.endurance,
    }


def get_bullet_type(name: str) -> tuple[str, int, tuple[int, int]]:
    """
    Get bullet parameters by name
    Returns tuple: (texture_file, radius, (vx, vy))
    """
    a = BulletTypes.get(BulletTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "radius": a.radius,
        "vx_vy": (a.vx, a.vy),
        "speed": a.speed,
        "enemy": a.enemy
    }


def get_saved_objects():
    objects = []
    for el in SavedObjects.select():
        objects.append({"object": el.object,
                        "object_type": el.object_type,
                        "object_position": (float(el.object_position.split(", ")[0]),
                                            float(el.object_position.split(", ")[1])),
                        "object_hp": el.object_hp,
                        "object_damage": el.object_damage
                        })
    return objects


def get_saved_game():
    for el in SavedGame.select():
        objects = {"player_x": el.player_x,
                   "player_y": el.player_y,
                   "player_hp": el.player_hp,
                   "level": el.level}
    return objects


def set_saved_objects(name, objects):
    for e in objects:
        n = SavedObjects.create(object=name, object_type=e.my_type,
                                object_position=str(e.x) + ", " + str(e.y),
                                object_hp=e.hp, object_damage=e.damage)
        n.save()


def set_saved_game(cur_level, player):
    n = SavedGame.create(
        player_x=player.x, player_y=player.y, player_hp=player.hp, level=cur_level
    )
    n.save()


def delete_saved_objects():
    for e in SavedObjects.select():
        SavedObjects.delete_by_id(e)
        SavedObjects.update()
    for e in SavedGame.select():
        SavedGame.delete_by_id(e)
        SavedGame.update()
