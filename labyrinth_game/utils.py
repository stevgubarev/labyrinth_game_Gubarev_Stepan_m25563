"""Вспомогательные функции: описание комнат и помощь."""

from labyrinth_game.constants import COMMANDS, ROOMS


def describe_current_room(game_state: dict) -> None:
    """Печатает описание текущей комнаты, предметы, выходы и наличие загадки."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room["description"])

    items = room["items"]
    if items:
        print("Заметные предметы:", ", ".join(items))

    exits = room["exits"]
    if exits:
        print("Выходы:", ", ".join(exits.keys()))

    if room["puzzle"] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def show_help(commands: dict[str, str] = COMMANDS) -> None:
    """Печатает список команд."""
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} - {desc}")

