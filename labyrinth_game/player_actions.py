"""Действия игрока: ввод и инвентарь."""
from __future__ import annotations

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def get_input(prompt: str = "> ") -> str:
    """Безопасный ввод: при Ctrl+C / Ctrl+D возвращает quit."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state: dict) -> None:
    """Печатает содержимое инвентаря."""
    inventory: list[str] = game_state["player_inventory"]
    if not inventory:
        print("Инвентарь пуст.")
        return
    print("Инвентарь:", ", ".join(inventory))

def move_player(game_state: dict, direction: str) -> None:
    """Перемещает игрока в другую комнату, если выход существует."""
    direction = direction.strip().lower()
    current_room = game_state["current_room"]
    exits: dict[str, str] = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]

    # Проверка на вход в комнату сокровищ
    if next_room == "treasure_room":
        inventory: list[str] = game_state["player_inventory"]
        if "rusty_key" in inventory:
            print(
                  "Вы используете найденный ключ, чтобы открыть путь " 
                  "в комнату сокровищ."
            )
        else:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return

    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1
    describe_current_room(game_state)
    random_event(game_state)

def _normalize_item_name(item_name: str) -> str:
    """Нормализует имя предмета: пробелы -> _, нижний регистр."""
    return "_".join(item_name.strip().lower().split())


def take_item(game_state: dict, item_name: str) -> None:
    """Подбирает предмет из комнаты в инвентарь."""
    item = _normalize_item_name(item_name)
    room = ROOMS[game_state["current_room"]]
    items: list[str] = room["items"]

    if item == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item not in items:
        print("Такого предмета здесь нет.")
        return

    items.remove(item)
    game_state["player_inventory"].append(item)
    print(f"Вы подняли: {item}")


def use_item(game_state: dict, item_name: str) -> None:
    """Использует предмет из инвентаря (если он есть)."""
    item = _normalize_item_name(item_name)
    inventory: list[str] = game_state["player_inventory"]

    if item not in inventory:
        print("У вас нет такого предмета.")
        return

    if item == "torch":
        print("Вы зажигаете факел. Вокруг становится светлее.")
        return

    if item == "sword":
        print("Вы крепче сжимаете меч. Теперь вы чувствуете уверенность.")
        return

    if item == "bronze_box":
        if "rusty_key" not in inventory:
            inventory.append("rusty_key")
            print("Вы открываете бронзовую шкатулку и находите rusty_key!")
        else:
            print("Шкатулка пуста — вы уже забрали всё ценное.")
        return

    print("Вы не знаете, как использовать этот предмет.")

