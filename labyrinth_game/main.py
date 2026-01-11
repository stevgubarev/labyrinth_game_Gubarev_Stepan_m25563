#!/usr/bin/env python3
"""Точка входа: запуск игры и базовый цикл команд."""

from __future__ import annotations

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command_line: str) -> None:
    """Обрабатывает команды пользователя."""
    raw = command_line.strip()
    if not raw:
        return

    parts = raw.split()
    command = parts[0].lower()
    arg = " ".join(parts[1:]) if len(parts) > 1 else ""

    # Односложные направления без go
    if command in {"north", "south", "east", "west"}:
        move_player(game_state, command)
        return

    match command:
        case "help":
            show_help(COMMANDS)
        case "look":
            describe_current_room(game_state)
        case "inventory" | "inv":
            show_inventory(game_state)
        case "go":
            if not arg:
                print("Укажите направление: go north/south/east/west")
                return
            move_player(game_state, arg)
        case "take":
            if not arg:
                print("Укажите предмет: take <item>")
                return
            take_item(game_state, arg)
        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "use":
            if not arg:
                print("Укажите предмет: use <item>")
                return
            use_item(game_state, arg)
        case "quit" | "exit":
            print("До встречи в лабиринте!")
            game_state["game_over"] = True
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

