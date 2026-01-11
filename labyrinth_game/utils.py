"""Вспомогательные функции: описание комнат и помощь."""

import math

from labyrinth_game.constants import (
    COMMANDS,
    EVENT_PROBABILITY_MODULO,
    EVENT_TRIGGER_VALUE,
    EVENT_VARIANTS,
    PUZZLE_REWARDS,
    ROOMS,
    TRAP_DAMAGE_MODULO,
    TRAP_DEATH_THRESHOLD,
)


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

def solve_puzzle(game_state: dict) -> None:
    """Решение загадки в текущей комнате. За успех выдаёт награду."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]
    puzzle = room["puzzle"]

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, answers = puzzle
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()

    normalized_answers = {a.strip().lower() for a in answers}
    if user_answer in normalized_answers:
        print("Верно! Вы решили загадку.")
        room["puzzle"] = None

        reward = PUZZLE_REWARDS.get(room_name)
        if reward is not None:
            if reward not in game_state["player_inventory"]:
                game_state["player_inventory"].append(reward)
            print(f"Награда получена: {reward}")
        return

    print("Неверно. Попробуйте снова.")

    if room_name == "trap_room":
         trigger_trap(game_state)

def attempt_open_treasure(game_state: dict) -> None:
    """Пытается открыть сундук в комнате сокровищ: ключом или кодом."""
    room_name = game_state["current_room"]
    room = ROOMS[room_name]

    if room_name != "treasure_room":
        print("Здесь нет сундука с сокровищами.")
        return

    if "treasure_chest" not in room["items"]:
        print("Сундук уже открыт.")
        return

    inventory: list[str] = game_state["player_inventory"]
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    answer = input("Сундук заперт. Ввести код? (да/нет) ").strip().lower()
    if answer != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = room["puzzle"]
    if puzzle is None:
        print("Кодовый механизм не активен.")
        return

    _, answers = puzzle
    code = input("Введите код: ").strip().lower()
    normalized_answers = {a.strip().lower() for a in answers}

    if code in normalized_answers:
        print("Код верный! Замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    print("Код неверный.")

def pseudo_random(seed: int, modulo: int) -> int:
    """Детерминированный псевдослучайный int в диапазоне [0, modulo)."""
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(frac * modulo)


def trigger_trap(game_state: dict) -> None:
    """Срабатывание ловушки: потеря предмета или шанс поражения."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory: list[str] = game_state["player_inventory"]
    if inventory:
        index = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    damage_roll = pseudo_random(game_state["steps_taken"], TRAP_DAMAGE_MODULO)
    if damage_roll < TRAP_DEATH_THRESHOLD:
        print("Вы не успели увернуться... Вы проиграли.")
        game_state["game_over"] = True
        return

    print("Вам повезло: вы уцелели!")


def random_event(game_state: dict) -> None:
    """Иногда запускает случайное событие после перемещения."""
    roll = pseudo_random(game_state["steps_taken"], EVENT_PROBABILITY_MODULO)
    if roll != EVENT_TRIGGER_VALUE:
        return

    event_type = pseudo_random(game_state["steps_taken"] + 1, EVENT_VARIANTS)

    room = ROOMS[game_state["current_room"]]
    inventory: list[str] = game_state["player_inventory"]

    if event_type == 0:
        print("Вы замечаете на полу монетку.")
        if "coin" not in room["items"]:
            room["items"].append("coin")
        return

    if event_type == 1:
        print("Вы слышите шорох где-то рядом...")
        if "sword" in inventory:
            print("Вы показываете меч — существо отступает.")
        return

    # event_type == 2
    if game_state["current_room"] == "trap_room" and "torch" not in inventory:
        print("В темноте вы наступаете на подозрительную плиту...")
        trigger_trap(game_state)

