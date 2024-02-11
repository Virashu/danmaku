"""Functions for work with database."""

from typing import Iterable
from danmaku.database.models import (
    Settings,
    db,
    BulletTypes,
    EnemyTypes,
    PlayerTypes,
    SavedObjects,
    SavedGame,
)


def get_enemy_type(name: str) -> dict:
    """
    Get enemy parameters by name
    Returns dict:
        {"texture_file", "texture_size", "speed", "shoot_v", "hp", "dm", "endurance"}
    """
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
        "cost": a.cost,
    }


def get_player_type(name) -> dict:
    """
    Get player parameters by name
    Returns dict: {"texture_file", "texture_size", "speed", "shoot_v", "hp", "dm",
         "endurance", "hitbox_radius"}
    """
    a = PlayerTypes.get(PlayerTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "texture_size": (a.texture_size_width, a.texture_size_height),
        "speed": a.speed,
        "shoot_v": a.shoot_v,
        "hp": a.hp,
        "dm": a.dm,
        "endurance": a.endurance,
        "hitbox_radius": a.hitbox_radius,
    }


def get_bullet_type(name: str) -> dict:
    """
    Get bullet parameters by name
    Returns dict: {"texture_file", "texture_size", "hitbox_radius", "vx_vy", "speed", "enemy"}
    """
    a = BulletTypes.get(BulletTypes.name == name)
    return {
        "texture_file": a.texture_file,
        "texture_size": (a.texture_size_width, a.texture_size_height),
        "hitbox_radius": a.hitbox_radius,
        "vx_vy": (a.vx, a.vy),
        "speed": a.speed,
        "enemy": a.enemy,
    }


def get_saved_objects() -> list:
    """Get saved objects from database"""
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


def get_saved_game() -> dict:
    """Get saved game from database
    Returns dict: {"score", "level", "power"}
    """
    game = tuple(iter(SavedGame.select().dicts()))[-1]
    return game


def get_game_history() -> list:
    """Get game history from database
    Returns list: [{"score", "level"}]
    """
    games = tuple(iter(SavedGame.select()))
    res = []
    for i in games:
        objects = {
            "score": i.score,
            "level": i.level,
        }
        res.append(objects)
    return res


def set_saved_objects(name: str, objects: Iterable) -> None:
    """Set saved objects to database"""
    for e in objects:
        n = SavedObjects.create(
            object=name,
            object_type=e.my_type,
            object_position=f"{e.x}, {e.y}",
            object_hp=e.health,
            object_damage=e.damage,
        )
        n.save()


def set_saved_game(cur_level: int, score: int, power: int) -> None:
    """Set saved game to database"""
    n = SavedGame.create(score=score, level=cur_level, power=power)
    n.save()


def delete_saved_objects() -> None:
    """Delete all saved objects from database"""
    for e in SavedObjects.select():
        SavedObjects.delete_by_id(e)
        SavedObjects.update()


def get_settings() -> dict:
    settings = {}
    for setting in Settings.select():
        match setting.type:
            case "int":
                value = int(setting.value)
                possible_values = list(map(int, setting.possible_values.split(";")))
            case "bool":
                value = bool(setting.value)
                possible_values = [True, False]
            case "str":
                value = setting.value
                possible_values = setting.possible_values.split(";")

        settings[setting.name] = {
            "display_name": setting.display_name,
            "possible_values": possible_values,
            "value": value,
        }

    return settings


def delete_settings():
    for setting in Settings.select():
        Settings.delete_by_id(setting)
        Settings.update()


def set_settings(settings: dict) -> None:
    for key, value in settings.items():
        s = Settings.get(Settings.name == key)
        s.value = value
        s.save()


if __name__ == "__main__":
    print(get_saved_game())
