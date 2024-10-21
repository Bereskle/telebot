import asyncio, os, json

from aiogram import Bot, Dispatcher, types, F
from random import randint
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


### Мой код ###
#import login as lp

#############################################
#  login и добавление к бд                                           READY
#  Возможность добавления материалов к базе                          READY
#  Добавить систему хэштегов
#  Добавить интерфейс для добавления фото и видео через тг чат
#  Попробовать реализовать рекомендации

#############################################

class RegisterFSM(StatesGroup): #Хз что это, но оно работает
    nickname_input = State()
    pass_input = State()


dir = { 
    'img_dir': './Image',
    'video_dir': './video'
}
#img = os.listdir(dir['img_dir'])
Token = 'some_token'
bot = Bot(token = Token)
dp = Dispatcher()
login =''
password = ''

sudo = False #Права


@dp.message(Command("start")) 
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    if sudo == True:
        file_img = json.load(open('img.json', 'r'))
        if message.photo[-1].file_id in file_img.values():
            await message.answer('Такое уже есть')
        else:
            file_img['img_id_'+str(len(file_img.keys()))] = message.photo[-1].file_id
            json.dump(file_img, open('img.json', mode='w', encoding='utf-8'))
    else:
       await message.answer("Не достаточно прав")
@dp.message(Command('login_admin')) 
async def on_login(message: types.Message, state: FSMContext):
    if sudo == True:
        await message.answer("Вы уже авторизованы")
    else:
        await message.answer("Введите логин")
        await state.set_state(RegisterFSM.nickname_input)

@dp.message(RegisterFSM.pass_input) #password
async def input_pass(message: types.Message, state: FSMContext):
    global password
    global sudo
    password = str(message.text)
    print(login+' '+  password +' '+ str(type(password)))
    with open('./lp.json') as f:
        templates = json.load(f)
        if (login.strip() in templates.keys()) and templates[login]["password"] == password.strip():
            await message.answer("Успех")
            sudo = True
        else:
            await message.answer("Try again")
    await state.clear() 



@dp.message(RegisterFSM.nickname_input) #login
async def input_nick(message: types.Message, state: FSMContext):
    global login 
    login = str(message.text)
    print(login, type(login))
    await message.answer("Введите пароль")
    await state.set_state(RegisterFSM.pass_input)

@dp.message(Command('help')) 
async def on_help(message: types.Message):
    await message.answer("Это помощь для бота.")

@dp.message(Command('img')) #обработка фото
async def img_send(message: types.Message):
    file_img = json.load(open('img.json', 'r'))
    await bot.send_photo(chat_id=message.chat.id, photo=file_img['img_id_' + str(randint(0, len(file_img)-1))])


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
   asyncio.run(main())
