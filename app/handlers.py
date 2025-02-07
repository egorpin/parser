from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.database.requests as rq
import app.states as states
import app.keyboards as kb
import app.texts as texts

import app.config as config

router = Router()

@router.message(CommandStart())
async def register(message: Message, state: FSMContext):
    if not await rq.user_exists(message.from_user.id):
        await rq.create_user(message.from_user.id)

    await state.set_state(states.Register.interval)
    await message.answer(texts.greetings, reply_markup=kb.notification_interval)

@router.message(F.text == "Изменить настройки")
async def change_settings(message: Message, state: FSMContext):
    await state.set_state(states.Register.interval)
    await message.answer(texts.notification_interval, reply_markup=kb.notification_interval)

@router.message(states.Register.interval)
async def register_interval(message: Message, state: FSMContext):
    await state.update_data(interval=message.text)

    await state.set_state(states.Register.tags)
    await message.answer(texts.taglist, reply_markup=kb.make_taglist())

@router.callback_query(states.Register.tags)
async def register_taglist(callback: CallbackQuery, state: FSMContext):
    tag = callback.data
    data = await state.get_data()
    tags = data.get('tags', [])

    if tag != 'cancel':
        tags.append(tag)

        await state.update_data(tags=tags)
        await callback.message.edit_reply_markup(reply_markup=kb.make_taglist(*tags))

    if len(tags) == len(config.categories) or tag == 'cancel':
        await rq.update_user(callback.from_user.id, interval_hours=config.notification_interval[data['interval'].lower()], tags=tags)
        await callback.answer()
        await callback.message.answer(texts.finish_registration.format(interval=data['interval'], tags='\n'.join(tags)), reply_markup=kb.default)

        await state.clear()
