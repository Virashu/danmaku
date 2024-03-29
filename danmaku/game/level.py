"""

Game contains levels
Level contains stages
Stage contains enemies and/or boss

"""

from typing import Any
import pygame

from danmaku.game.enemy import Enemy


class Stage:
    """Base stage

    Contains enemies"""

    _enemies: list[Enemy]

    _start_time: int
    # appearance of enemies can be bound to time

    def __init__(self, enemies: list[Enemy]) -> None:
        self._enemies = list(enemies)

        self._start_time = pygame.time.get_ticks()

    def update(self) -> None:
        """WIP

        Update all enemies on the stage"""

    @property
    def enemies(self) -> list[Enemy]:
        """Enemies on the stage"""
        return self._enemies


class BossStage(Stage):
    """Stage centered on boss"""

    # +enemies: list[Enemy]
    _boss: Enemy

    ## Boss actions ##
    # Boss actions are bound to time passed from stage start
    # Actions are being stored in tuples in format:
    # (time in milliseconds, action, args)

    # ( 1000, "move_to", (10, 20) )
    # ( 2000, "shoot_radial", () )

    def __init__(
        self,
        enemies: list[Enemy],
        boss: Enemy,
        actions: list[tuple[int, str, tuple[Any]]],
    ) -> None:
        super().__init__(enemies)
        self._boss = boss
        self._actions = list(actions)

    def update(self) -> None:
        if self._actions:
            if pygame.time.get_ticks() - self._start_time >= self._actions[0][0]:
                print(f"Function: {self._actions[0][1]}\tArgs: {self._actions[0][2]}")
                self._actions.pop(0)

    @property
    def boss(self) -> Enemy:
        """Boss property"""
        return self._boss

    @property
    def enemies(self) -> list[Enemy]:
        return self._enemies + [self._boss]


class Level:
    """Game level

    Contains stages
    For chapter separation by theme
    (can contain only one boss, but with multiple boss stages)"""

    stages: list[Stage]
    current_stage: int

    enemies: list[Enemy]  # enemies from current stage

    def __init__(self, stages: list[Stage]) -> None:
        self.stages = list(stages)
        self.current_stage = 0
        self.enemies = list(self.stages[self.current_stage].enemies)

    def __len__(self) -> int:
        return len(self.stages)

    def __getitem__(self, index: int) -> Stage:
        return self.stages[index]

    @property
    def stage(self) -> Stage:
        """Current stage"""
        return self.stages[self.current_stage]

    def next_stage(self) -> bool:
        """Switch stage to next if possible

        Returns: bool - success"""
        if len(self.stages) > self.current_stage + 1:
            self.current_stage += 1
            self.enemies = list(self.stages[self.current_stage].enemies)
            return True
        return False

    def set_stage(self, index: int) -> None:
        """Set stage by index"""
        self.current_stage = index
        self.enemies = list(self.stages[self.current_stage].enemies)
