"""Application entry point."""

from vgame import Runner

from danmaku.menu import Menu
from danmaku.game import Game
from danmaku.history import History
from danmaku.settings import Settings

WIDTH, HEIGHT = 300, 500


runner = Runner()

while runner.running:
    menu = Menu(width=WIDTH, height=HEIGHT, title="Danmaku | Menu")
    runner.run(menu)
    match menu.exit_status:
        case "game_new":
            runner.run(Game(width=WIDTH, height=HEIGHT, title="Danmaku | Game"))
        case "game_continue":
            game = Game(width=WIDTH, height=HEIGHT, title="Danmaku | Game")
            game.new_game = False
            runner.run(game)
        case "settings":
            settings = Settings(width=WIDTH, height=HEIGHT, title="Danmaku | Settings")
            runner.run(settings)
        case "history":
            history = History(width=WIDTH, height=HEIGHT, title="Danmaku | History")
            runner.run(history)

