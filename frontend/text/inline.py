from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


buttons = []
keyboards = []

for i in range(10):
    buttons.append(InlineKeyboardButton(str(i + 1), callback_data=f"b{i}"))


def choose_city_button(count: int):
    choose_city_kb = InlineKeyboardMarkup()
    if count < 5:
        choose_city_kb.row(*buttons[:count])
    else:
        count -= 1
        j = int(count / 2) + 1
        choose_city_kb.row(*buttons[:j])
        choose_city_kb.row(*buttons[j:count + 1])
    return choose_city_kb


