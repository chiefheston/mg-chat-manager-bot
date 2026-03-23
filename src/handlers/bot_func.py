from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import bot
from constants import (
    CANCEL,
    CHAT_INFO,
    CMD_ADD_USER,
    CMD_CACNEL,
    CMD_REMOVE_USER,
    ERRORS,
    ERRORS_IN,
    GEN_INVITE_FOR_CHATS,
    GIVE_ME_TG_ID,
    JOIN_LATER,
    JOIN_NOW,
    NOTHING,
    NOT_FOUND_FROM,
    NO_CHANGE,
    ONLY_ADMIN,
    PRIORITY,
    REMOVE_FROM,
    USER_ID_NOT_CORRECT,
)
from states.bot_func import DeleteUserForm, UserForm
from validators import is_admin

router = Router()


async def get_user_id_check_command(
    message: Message,
) -> int | None:
    """Take user_id from command and checks for admin rights."""
    if not await is_admin(message.from_user.id):
        await message.answer(ONLY_ADMIN)
        return None
    user_input = message.text.strip()
    try:
        return int(user_input)
    except ValueError:
        await message.answer(USER_ID_NOT_CORRECT)
        return None


async def send_invites_to_user(user_id: int) -> Tuple[List[str], List[str]]:
    """Send invite links to user for all chats."""
    priority_links: List[str] = []
    other_links: List[str] = []
    errors: List[str] = []
    for chat_id, info in CHAT_INFO.items():
        try:
            await bot.unban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                only_if_banned=True,
            )
            invite = await bot.create_chat_invite_link(
                chat_id=chat_id,
                expire_date=datetime.now(timezone.utc) + timedelta(days=2),
            )
            entry = f'{info["name"]}:\n{invite.invite_link}'
            if info.get(PRIORITY):
                priority_links.append(entry)
            else:
                other_links.append(entry)
        except TelegramBadRequest as error:
            errors.append(f'{chat_id}: {error.message}')
    parts: List[str] = []
    if priority_links:
        parts.append(
            JOIN_NOW + '\n'.join(f'— {lnk}' for lnk in priority_links),
        )
    if other_links:
        parts.append(
            JOIN_LATER + '\n'.join(f'— {lnk}' for lnk in other_links),
        )
    if parts:
        try:
            await bot.send_message(
                chat_id=user_id,
                text='\n\n'.join(parts),
                disable_web_page_preview=True,
            )
        except TelegramBadRequest as error:
            errors.append(f'send_message to {user_id}: {error.message}')
    return priority_links + other_links, errors


@router.callback_query(F.data.startswith(CMD_ADD_USER))
async def cmd_add_user(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Command /add_user."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        GIVE_ME_TG_ID,
    )
    await state.set_state(UserForm.tg_id)


@router.message(UserForm.tg_id)
async def proc_tg_id(
    message: Message,
    state: FSMContext,
) -> None:
    """Take ID and adds to chats."""
    if message.text == CANCEL:
        await cmd_cancel(message, state)
        return
    report: List = []
    user_id = await get_user_id_check_command(message)
    if not user_id:
        return
    invite_links, errors = await send_invites_to_user(user_id)
    if invite_links:
        report.append(GEN_INVITE_FOR_CHATS)
        report.extend(invite_links)
    if errors:
        report.append(ERRORS)
        report.extend(errors)
    await message.answer(
        '\n'.join(report) if report else NOTHING,
    )
    await state.clear()
    await message.delete()


@router.callback_query(F.data.startswith(CMD_REMOVE_USER))
async def cmd_remove_user(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    """Command /remove_user."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        GIVE_ME_TG_ID,
    )
    await state.set_state(DeleteUserForm.tg_id)


@router.message(DeleteUserForm.tg_id)
async def proc_tg_id_remove(
    message: Message,
    state: FSMContext,
) -> None:
    """Take ID and deletes from chats."""
    if message.text == CANCEL:
        await cmd_cancel(message, state)
        return
    user_id = await get_user_id_check_command(message)
    removed, not_found, errors = [], [], []
    for chat_id, info in CHAT_INFO.items():
        chat_name = info['name']
        try:
            await bot.ban_chat_member(chat_id, user_id)
            removed.append(chat_name)
        except TelegramBadRequest as error:
            desc = error.args[0].lower()
            if 'not participant' in desc or 'user not found' in desc:
                not_found.append(chat_name)
            else:
                errors.append(f'{chat_name}: {error.message}')
    report: List = []
    if removed:
        report.append(REMOVE_FROM + '\n— '.join(removed))
    if not_found:
        report.append(NOT_FOUND_FROM.join(not_found))
    if errors:
        report.append(ERRORS_IN.join(errors))
    await message.answer(
        '\n\n'.join(report) if report else NO_CHANGE,
    )
    await state.clear()
    await message.delete()


@router.message(Command(CMD_CACNEL))
async def cmd_cancel(
    message: Message,
    state: FSMContext,
) -> None:
    """Cancel all."""
    await message.delete()
    await state.clear()
    await message.answer('Все действия отменены.')
