#!/usr/bin/env python3
"""Точка входа: запуск игры и базовый цикл команд."""

from __future__ import annotations

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import get_input, show_inventory
from labyrinth_game.utils import describe_current_room, show_help


def process_command(game_state: dict, command_line: str) -> None:
    """Обрабатывает базовые команды (пока без движения и предметов)."""
    command = command_line.strip().lower()

    match command:
        case "help":
            show_help(COMMANDS)
        case "look":
            describe_current_room(game_state)
        case "inventory" | "inv":
            show_inventory(game_state)
        case "quit" | "exit":
            print("До встречи в лабиринте!")
            game_state["game_over"] = True
        case "":
            return
        case _:
            print("Неизвестная команда. Введите help для списка команд.")


def main() -> None:
    """Запуск игры."""
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    show_help(COMMANDS)

    while not game_state["game_over"]:
        command_line = get_input("> ")
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()

