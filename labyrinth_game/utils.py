"""Вспомогательные функции: описание комнат и помощь."""

from labyrinth_game.constants import COMMANDS, PUZZLE_REWARDS, ROOMS


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

