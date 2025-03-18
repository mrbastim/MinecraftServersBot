import psutil
from psutil._common import bytes2human
import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode 
from config import ADMIN_ID
from service_manager import ServiceManager
import keyboards

router = Router()

async def disk_usage():
    templ = "%-17s %8s %8s %8s %5s%% %9s  %s\n"
    output = templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount")

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        output += templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint
        )

    return output

async def send_system_info(message: Message):
    try:
        cpu_percent = psutil.cpu_percent(interval=1) 
        ram = psutil.virtual_memory()
        ram_percent = ram.percent 

        system_info = f"""CPU Usage: {cpu_percent}%
RAM Usage: {ram_percent}%
"""
        disk_percent = await disk_usage()
        delimiter = '+' + '-'*40 + '+'
        await message.edit_text(text=f"<pre>{delimiter}\n{system_info}{delimiter}\n{disk_percent}{delimiter}</pre>",
                                    parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply(f"Error \- `{e}`", parse_mode="MarkdownV2")

@router.message(CommandStart())
async def on_start(message: Message):
    await message.answer("Привет! Я бот для управления майнкрафт серверами.", reply_markup=keyboards.main_menu)

@router.message(F.text=="🛠 Доступные сервера")
async def server_list_handler(message: Message):
    await message.answer("Выберите сервер:", reply_markup=await keyboards.get_server_list_keyboard())

@router.message(F.text=="📊 Информация о загрузке сервера")
async def server_info_handler(message: Message):
    await send_system_info(await message.answer("Получение информации..."))

@router.callback_query(lambda callback: callback.data == "back_to_services")
async def back_to_services_handler(callback: CallbackQuery):
    await callback.message.edit_text("Выберите сервер:", reply_markup=await keyboards.get_server_list_keyboard())
    await callback.answer()

@router.callback_query(lambda callback: callback.data.endswith("Server"))
async def process_server_callback(callback: CallbackQuery):
    server_name = callback.data
    server = ServiceManager(server_name)
    status = server.get_status()
    choice_keyboard = await keyboards.get_choice_keyboard(server_name)
    await callback.message.edit_text(
        text = f"Статус сервера {server_name}:\n <b>{status}</b>", 
        parse_mode=ParseMode.HTML, 
        reply_markup=choice_keyboard
    )
    await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("start_"))
async def start_server_handler(callback: CallbackQuery):
    server_name = callback.data[len("start_"):]
    server = ServiceManager(server_name)
    result = server.start_service()
    choice_keyboard = await keyboards.get_choice_keyboard(server_name)
    await callback.message.edit_text(
        text=f"Результат запуска сервера {server_name}:\n <b>{result}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=choice_keyboard
    )
    await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("stop_"))
async def stop_server_handler(callback: CallbackQuery):
    server_name = callback.data[len("stop_"):]
    server = ServiceManager(server_name)
    result = server.stop_service()
    choice_keyboard = await keyboards.get_choice_keyboard(server_name)
    await callback.message.edit_text(
        text=f"Результат остановки сервера {server_name}:\n <b>{result}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=choice_keyboard
    )
    await callback.answer()

