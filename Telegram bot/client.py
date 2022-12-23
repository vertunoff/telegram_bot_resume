from typing import Text
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types.input_file import InputFile
from utils import translate
from create_document import create_docx
import string, random

import os


storage = MemoryStorage()
bot = Bot(token='5608205852:AAFnDjh4XtJiwx0I-20vgo_WReaLl5dD0EA')
dp = Dispatcher(bot, storage=storage) 

async def on_startup(_):
    print('Bot launched')

gender_male = KeyboardButton('Мужской')
gender_female = KeyboardButton('Женский')

yes = KeyboardButton('Да')
no = KeyboardButton('Нет')

full = KeyboardButton("Полная")
nfull = KeyboardButton("Неполная")

full2 = KeyboardButton("Полный")
nfull2 = KeyboardButton("Неполный")
short = KeyboardButton('Сокращенный')
floating = KeyboardButton('Гибкий')

halfedu = KeyboardButton('Среднее')
halfprof = KeyboardButton('Среднее профессиональное')
high = KeyboardButton('Высшее')

g_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
g_keyboard.add(gender_male).add(gender_female)

yesno_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yesno_keyboard.add(yes).add(no)

activ_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
activ_keyboard.add(full).add(nfull)

graph_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
graph_keyboard.add(full2).add(nfull2).add(short).add(floating)

ed_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
ed_keyboard.add(no).add(halfedu).add(halfprof).add(high)

class Get_Data(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()
    profession = State()
    occup = State()
    graph = State()
    salary = State()
    phone = State()
    mail = State()
    country = State()
    city = State()
    relation = State()
    education = State()
    school = State()
    graduate = State()
    faculty = State()
    speciality = State()
    form = State()
    exp = State()
    worktime = State()
    role = State()
    organisation = State()
    achivements = State()
    foreign = State()
    drive = State()
    army = State()
    hobby = State()
    personality = State()


@dp.message_handler(commands=['start'])
async def start(message : Message):
    name, lname = message.from_user.first_name, message.from_user.last_name
    if lname:
        s = f'Добро пожаловать, {name} {lname}!\n'
    else:
        s = f'Добро пожаловать, {name}!\n'
    s += 'Бот позволяет создать резюме для приема на работу.'
    await bot.send_message(message.from_user.id, s, reply_markup=keyboard)

@dp.message_handler(commands=['Анкета', 'resume', 'r'], state=None)
async def r_start(message : Message):
    await Get_Data.name.set()
    await message.answer("Заполнение анкеты. Для выхода напишите \"отмена\"")
    await message.answer('Введите ФИО', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_resume(message : Message, state : FSMContext):
    current_state = await state.get_data()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Заполнение анкеты отменено')


@dp.message_handler(state=Get_Data.name)
async def load_name(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Get_Data.next()
    await message.answer('Введите дату рождения')

@dp.message_handler(state=Get_Data.age)
async def load_age(message : Message, state: FSMContext):
    age = message.text
    async with state.proxy() as data:
                data['Дата рождения'] = age
    await Get_Data.next()
    await message.answer('Выберите пол', reply_markup=g_keyboard)

@dp.message_handler(state=Get_Data.gender)
async def load_gender(message : Message, state: FSMContext):
    gender = message.text
    if gender.lower() not in ('мужской', 'женский'):
        await message.answer('Выберите пол', reply_markup=g_keyboard)
        return
    async with state.proxy() as data:
        data['Пол'] = gender.lower()
    await Get_Data.next()
    await message.answer('Отправьте Ваше фото', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(content_types=['photo', 'document'], state=Get_Data.photo)
async def load_photo(message : Message, state: FSMContext):
    async with state.proxy() as data:
        if message.photo:
            photo = message.photo[-1]
            data['photo'] = photo

        else:
            photo = message.document
            data['photo'] = photo
        
    await Get_Data.next()
    await message.answer('Желаемая профессия')

@dp.message_handler(state=Get_Data.profession)
async def load_profession(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Профессия'] = message.text
    await Get_Data.next()
    await message.answer('Занятость (полная/неполная)', reply_markup=activ_keyboard)

@dp.message_handler(state=Get_Data.occup)
async def load_occup(message : Message, state: FSMContext):
    if message.text.lower() not in ('полная', 'неполная'):
        await message.answer('Занятость (полная/неполная)', reply_markup=activ_keyboard)
        return
    async with state.proxy() as data:
        data['Занятость'] = message.text.lower()
    await Get_Data.next()
    await message.answer('График работы: (полный/неполный/сокращённый/гибкий)', reply_markup=graph_keyboard)
    
@dp.message_handler(state=Get_Data.graph)
async def load_graph(message : Message, state: FSMContext):
    if message.text.lower() not in ('полный', 'неполный','сокращённый', 'сокращенный', 'гибкий'):
        await message.answer('График работы: (полный/неполный/сокращённый/гибкий)', reply_markup=graph_keyboard)
        return
    async with state.proxy() as data:
        data['График работы'] = message.text.lower()
    await Get_Data.next()
    await message.answer('Желаемая зарплата', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Get_Data.salary)
async def load_salary(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Желаемая зарплата'] = message.text
    await Get_Data.next()
    await message.answer('Ваш телефон')
    
@dp.message_handler(state=Get_Data.phone)
async def load_phone(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Телефон'] = message.text
    await Get_Data.next()
    await message.answer('Ваша электронная почта')

@dp.message_handler(state=Get_Data.mail)
async def load_mail(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Электронная почта'] = message.text.lower()
    await Get_Data.next()
    await message.answer('Заполните личную информацию')
    await message.answer('Гражданство')


@dp.message_handler(state=Get_Data.country)
async def load_country(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Гражданство'] = message.text.capitalize()
    await Get_Data.next()
    await message.answer('Место проживания')

@dp.message_handler(state=Get_Data.city)
async def load_city(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Место проживания'] = message.text.capitalize()
    await Get_Data.next()
    await message.answer('Семейное положение')
    

@dp.message_handler(state=Get_Data.relation)
async def load_relation(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Семейное положение'] = message.text.lower()
    await Get_Data.next()
    await message.answer('Образование', reply_markup=ed_keyboard)


@dp.message_handler(state=Get_Data.education)
async def load_education(message : Message, state: FSMContext):
    if message.text.lower() not in ('среднее', 'нет', 'среднее профессиональное', 'высшее'):
        await message.answer('Образование', reply_markup=ed_keyboard)
        return
    async with state.proxy() as data:
        data['Образование'] = message.text.lower()
        if data['Образование'] == 'нет':
            for _ in range(6):
                await Get_Data.next()
            await message.answer('Тяжеловато Вам будет')
            await message.answer('Ну... ладно')
            await message.answer('Нет так нет')
            await message.answer('Имеется ли у вас опыт работы?', reply_markup=yesno_keyboard)
            return
        await Get_Data.next()
    await message.answer('Учебное заведение', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Get_Data.school)
async def load_school(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Учебное заведение'] = message.text
    await Get_Data.next()
    await message.answer('Год окончания')

@dp.message_handler(state=Get_Data.graduate)
async def load_graduate(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Год окончания'] = message.text
        if data['Образование'] == "среднее":
            for _ in range(3):
                await Get_Data.next()
            await message.answer('Форма обучения')
            return
    await Get_Data.next()
    await message.answer('Факультет')

@dp.message_handler(state=Get_Data.faculty)
async def load_faculty(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Факультет'] = message.text
    await Get_Data.next()
    await message.answer('Специальность')

@dp.message_handler(state=Get_Data.speciality)
async def load_speciality(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Специальность'] = message.text
    await Get_Data.next()
    await message.answer('Форма обучения')

@dp.message_handler(state=Get_Data.form)
async def load_form(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Форма обучения'] = message.text.lower()
    await Get_Data.next()
    await message.answer('Имеется ли у вас опыт работы?', reply_markup=yesno_keyboard)


@dp.message_handler(state=Get_Data.exp)
async def load_exp(message : Message, state: FSMContext):
    exp = message.text.lower()
    if exp not in ('да', 'нет'):
        await message.answer('Имеется ли у вас опыт работы?', reply_markup=yesno_keyboard)
        return
    async with state.proxy() as data:
        if exp == 'да':
            data['exp'] = True
            await message.answer('Период работы', reply_markup=ReplyKeyboardRemove())
            await Get_Data.next()
        else:
            data['exp'] = False
            await message.answer('Заполните дополнительную информацию', reply_markup=ReplyKeyboardRemove())
            await message.answer('Инностранные языки')
            for _ in range(5):
                await Get_Data.next()


@dp.message_handler(state=Get_Data.worktime)
async def load_wortime(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Период работы'] = message.text
    await Get_Data.next()
    await message.answer('Должность')


@dp.message_handler(state=Get_Data.role)
async def load_role(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Должность'] = message.text
    await Get_Data.next()
    await message.answer('Организация')
    
@dp.message_handler(state=Get_Data.organisation)
async def load_organisation(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Организация'] = message.text
    await Get_Data.next()
    await message.answer('Должностные обязанности и достижения')

@dp.message_handler(state=Get_Data.achivements)
async def load_achivements(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Должностные обязанности и достижения'] = message.text
    await Get_Data.next()
    await message.answer('Заполните дополнительную информацию')
    await message.answer('Какими иностранными языками вы владеете?')

@dp.message_handler(state=Get_Data.foreign)
async def load_foreign(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Иностранные языки'] = message.text
    await Get_Data.next()
    await message.answer('Наличие водительских прав (если есть, то категория)')

@dp.message_handler(state=Get_Data.drive)
async def load_drive(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Наличие водительских прав'] = message.text
    await Get_Data.next()
    await message.answer('Служба в армии')

@dp.message_handler(state=Get_Data.army)
async def load_army(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Служба в армии'] = message.text
    await Get_Data.next()
    await message.answer('Увлечения, хобби, занятия в свободное время')

@dp.message_handler(state=Get_Data.hobby)
async def load_hobby(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Увлечения'] = message.text.lower()
    await Get_Data.next()
    await message.answer('Личные качества')


@dp.message_handler(state=Get_Data.personality)        
async def load_personality(message : Message, state: FSMContext):
    async with state.proxy() as data:
        data['Личные качества'] = message.text.lower()
        pic = data['photo']
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))+'.png'
        await pic.download(destination_file=filename)
        create_docx('temp.docx', data, filename)
        os.remove(filename)
    name : str = data['name']
    print(data.as_dict())
    file = InputFile('temp.docx', filename=f'resume_{"_".join(translate(name.lower()).split()[:2])}.docx')
    await bot.send_document(message.from_user.id, file)
    await state.finish()

b1 = KeyboardButton('/Анкета')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyboard.add(b1)







executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
