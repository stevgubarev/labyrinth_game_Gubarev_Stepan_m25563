"""Действия игрока: ввод и инвентарь."""

from __future__ import annotations


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

