"""Application entry point."""

from vgame import Runner

from danmaku.ui.menu import Menu
from danmaku.game.game import Game
from danmaku.ui.history import History
from danmaku.ui.settings import Settings
from danmaku.ui.game_end import GameEnd

WIDTH, HEIGHT = 500, 500
TICKRATE = 120


runner = Runner()


def run_game(is_new: bool):
    "Game exit handling"
    game = Game(width=WIDTH, height=HEIGHT, title="Danmaku | Game", tickrate=TICKRATE)
    game.new_game = is_new
    runner.run(game)

    match game.exit_status:
        case "win":
            end = GameEnd(
                width=WIDTH,
                height=HEIGHT,
                title="Danmaku | Game Over",
                tickrate=TICKRATE,
            )
            end.set("You win", (30, 157, 214), "sounds/win.wav")
            runner.run(end)
        case "lose":
            end = GameEnd(
                width=WIDTH,
                height=HEIGHT,
                title="Danmaku | Game Over",
                tickrate=TICKRATE,
            )
            end.set("Game over", (30, 157, 214), "sounds/lose.wav")
            runner.run(end)


while runner.running:
    menu = Menu(width=WIDTH, height=HEIGHT, title="Danmaku | Menu")
    runner.run(menu)
    match menu.exit_status:
        case "game", new_game:
            run_game(new_game)
        case "settings":
            settings = Settings(width=WIDTH, height=HEIGHT, title="Danmaku | Settings")
            runner.run(settings)
        case "history":
            history = History(width=WIDTH, height=HEIGHT, title="Danmaku | History")
            runner.run(history)
