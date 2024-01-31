from danmaku.database.models import *


def get_enemy_type(name):
    with db.atomic():
        a = EnemyTypes.get(EnemyTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "texture_size": (a.texture_size_width, a.texture_size_height),
        "speed": a.speed,
        "shoot_v": a.shoot_v,
        "hp": a.hp,
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
        "hp": a.hp,
        "dm": a.dm,
        "endurance": a.endurance,
    }


def get_bullet_type(name: str) -> dict:
    """
    Get bullet parameters by name
    Returns dict: {"texture_file", "radius", "vx_vy", "speed", "enemy"}
    """
    a = BulletTypes.get(BulletTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "radius": a.radius,
        "vx_vy": (a.vx, a.vy),
        "speed": a.speed,
        "enemy": a.enemy,
    }


def get_saved_objects():
    objects = []
    for el in SavedObjects.select():
        objects.append(
            {
                "object": el.object,
                "object_type": el.object_type,
                "object_position": (
                    float(el.object_position.split(", ")[0]),
                    float(el.object_position.split(", ")[1]),
                ),
                "object_hp": el.object_hp,
                "object_damage": el.object_damage,
            }
        )
    return objects


def get_saved_game():
    games = tuple(iter(SavedGame.select()))
    game = games[-1]
    objects = {
        "player_x": game.player_x,
        "player_y": game.player_y,
        "player_hp": game.player_hp,
        "level": game.level,
    }
    return objects


def set_saved_objects(name, objects):
    for e in objects:
        n = SavedObjects.create(
            object=name,
            object_type=e.my_type,
            object_position=str(e.x) + ", " + str(e.y),
            object_hp=e.hp,
            object_damage=e.damage,
        )
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
