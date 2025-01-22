from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

import app.database.requests as rq

import app.states as states
import app.keyboards as kb
import app.texts as texts

router = Router()

notification_interval = {'1 час': 1, '3 часа': 3, '6 часов': 6, '12 часов': 12, 'раз в день': 24, 'никогда': 0}

@router.message(CommandStart())
async def register(message: Message, state: FSMContext):
    if not await rq.user_exists(message.from_user.id):
        await rq.create_user(message.from_user.id)

    await state.set_state(states.Register.interval)
    await message.answer(texts.greetings, reply_markup=kb.notification_interval)

@router.message(states.Register.interval)
async def register_interval(message: Message, state: FSMContext):
    await state.update_data(interval=message.text)

    await state.set_state(states.Register.tags)
    await message.answer(texts.taglist, reply_markup=kb.taglist)

@router.callback_query(states.Register.tags)
async def register_taglist(callback: CallbackQuery, state: FSMContext):
    tag = callback.data
    data = await state.get_data()
    tags = data.get('tags', [])

    if tag == 'cancel':
        user = await rq.get_user(callback.from_user.id)
        user.interval_hours = notification_interval[data['interval'].lower()]
        user.tags = tags

        await rq.update_user(user)
        await callback.answer()
        await callback.message.answer(texts.finish_registration.format(data['interval'], user.tags))

        await state.clear()
        return

    tags.append(tag)

    await state.update_data(tags=tags)

    if len(tags) == 4:
        await callback.answer()
        await state.clear()
