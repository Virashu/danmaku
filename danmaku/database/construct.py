from danmaku.database.models import *


db.connect()
db.drop_tables([EnemyTypes])
db.create_tables([EnemyTypes])


basic_enemy = EnemyTypes.create(
    name="basic enemy",
    texture_file="basic_enemy_2.png;basic_enemy_1.png;"
    "basic_enemy_2.png;basic_enemy_3.png",
    texture_size_width=50,
    texture_size_height=65,
    speed=30,
    shoot_v=1500,
    hp=250,
    dm=50,
    endurance=0.1,
    cost=50
)
basic_enemy.save()

strong_enemy = EnemyTypes.create(
    name="strong enemy",
    texture_file="strong_enemy_2.png;strong_enemy_1.png;"
    "strong_enemy_2.png;strong_enemy_3.png",
    texture_size_width=50,
    texture_size_height=65,
    speed=20,
    shoot_v=1000,
    hp=250,
    dm=50,
    endurance=0.1,
    cost=100
)
strong_enemy.save()

boss = EnemyTypes.create(
    name="boss",
    texture_file="strong_enemy_2.png;strong_enemy_1.png;"
    "strong_enemy_2.png;strong_enemy_3.png",
    texture_size_width=60,
    texture_size_height=85,
    speed=10,
    shoot_v=500,
    hp=550,
    dm=70,
    endurance=0.3,
    cost=500
)
boss.save()


basic_enemy_bullet = BulletTypes.create(
    name="basic enemy bullet",
    enemy=True,
    texture_file="bullet.png",
    radius=10,
    speed=150,
    vx=0,
    vy=1,
)
basic_enemy_bullet.save()

basic_player_bullet = BulletTypes.create(
    name="basic player bullet",
    enemy=False,
    texture_file="bullet.png",
    radius=10,
    speed=150,
    vx=0,
    vy=-1,
)
basic_player_bullet.save()

player = PlayerTypes.create(
    name="player",
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
    texture_size_width=50,
    texture_size_height=50,
    speed=100,
    shoot_v=250,
    hp=1300,
    dm=500,
    endurance=1,
)
player.save()
