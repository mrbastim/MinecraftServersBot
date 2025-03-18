from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from service_manager import ServiceManager

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛠 Доступные сервера"),
            KeyboardButton(text="📊 Информация о загрузке сервера")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие..."
)

async def get_server_list_keyboard():
    servers = await ServiceManager.get_servers()
    keyboard = InlineKeyboardBuilder()
    for server in servers:
        keyboard.add(InlineKeyboardButton(text=server.name, callback_data=server.name))
    return keyboard.adjust(2).as_markup()

async def get_choice_keyboard(server_name: str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Запустить сервер", callback_data=f"start_{server_name}"),
        InlineKeyboardButton(text="Остановить сервер", callback_data=f"stop_{server_name}")
    )
    return keyboard.adjust(2).as_markup()