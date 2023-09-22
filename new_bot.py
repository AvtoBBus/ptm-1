import telebot
import config
import os.path
import time
import csv
import get_schedule as gs
import get_schedule_session as gs_session

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message) -> None:
    '''
    Функция приветствия с пользователем
    '''
    list_info = []
    with open("data/info.txt", encoding='utf-8') as file:
        list_info = file.readlines()

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("/change")
    markup.add(item1)

    sti = open('data/stickers/HI.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(
        message.chat.id, f"Приветик, {message.from_user.first_name}!\nЯ бот Эдди, призванный помогать в учёбе\n")

    bot.send_message(
        message.chat.id, list_info)

    received_message_text = bot.send_message(
        message.chat.id, "Нажми \"/change\" чтобы начать", reply_markup=markup)

    bot.register_next_step_handler(received_message_text, change_option)


@bot.message_handler(commands=['change'])
def change_option(message) -> None:
    '''
    Функция "выбора опции, где отрисовывается меню, а также проверется пользовался ли пользователь ботом"
    '''
    write_in_file = True
    with open("users.csv", "r", encoding="utf-8") as file:
        readerder = csv.reader(file, delimiter=";")
        for row in readerder:
            if row[1] == str(message.from_user.id):
                write_in_file = False
    if write_in_file:
        print(
            f"Новый пользователь -> {message.from_user.first_name} -> ID: {message.from_user.id}")
        with open("users.csv", "a", newline="", encoding="utf-8") as file:
            printer = csv.writer(file, delimiter=";")
            printer.writerow([
                message.from_user.first_name,
                message.from_user.id,
                message.chat.id
            ])

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Узнать задание по лабе")
    item2 = types.KeyboardButton("Достать учебник")
    item3 = types.KeyboardButton("Получить секретик")
    item4 = types.KeyboardButton("Узнать расписание")
    item5 = types.KeyboardButton("Важные ссылки")
    if str(message.from_user.id) == '765103434':
        item6 = types.KeyboardButton("News")
        markup.add(item1, item2, item3, item4, item5, item6)
    else:
        markup.add(item1, item2, item3, item4, item5)

    received_message_text = bot.send_message(
        message.chat.id, "Погнали!", reply_markup=markup)
    bot.register_next_step_handler(received_message_text, expanded_change)


@bot.message_handler(content_types=['text'])
def expanded_change(message) -> None:
    '''
    Выбор дальнейших дествий в зависимости от того, что выбрал пользователь в функции change_option
    '''
    if message.chat.type == 'private':
        if message.text == 'Узнать задание по лабе':
            sti1 = open('data/stickers/REALLY.webp', 'rb')
            bot.send_sticker(message.chat.id, sti1)
            markup = types.ReplyKeyboardRemove()
            list_items = []
            list_files = os.listdir("data/labs_book/labs/")
            list_files.sort()
            for files in list_files:
                list_items.append(files)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            for item in list_items:
                markup.add(item)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)
            received_message_text = bot.send_message(
                message.chat.id, "Что именно нужно?", reply_markup=markup)
            bot.register_next_step_handler(
                received_message_text, change_lab_task)

        elif message.text == 'Достать учебник':
            sti2 = open('data/stickers/YES.webp', 'rb')
            bot.send_sticker(message.chat.id, sti2)
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Окей', reply_markup=markup)

            list_items = []
            list_files = os.listdir("data/labs_book/")
            list_files.sort()
            for files in list_files:
                list_items.append(files)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            for item in list_items:
                if str(item) != "labs":
                    markup.add(item)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)

            received_message_text = bot.send_message(
                message.chat.id, "По какому предмету?", reply_markup=markup)
            bot.register_next_step_handler(received_message_text, change_book)

        elif message.text == 'Получить секретик':
            file = open("allowed_users.csv", "r", encoding="utf-8")
            readerder = csv.reader(file, delimiter=";")
            locked = True
            for row in readerder:
                if str(row[0]) == str(message.from_user.id):
                    locked = False
            if locked == False:
                received_message = bot.send_message(
                    message.chat.id, "Ура! У тебя есть доступ!\nНапиши, что угодно. чтобы продолжить!")
                bot.register_next_step_handler(received_message, change_secret)
            else:
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True, one_time_keyboard=True)
                item1 = types.KeyboardButton("/change")
                markup.add(item1)
                received_message = bot.send_message(
                    message.chat.id, "Блинб, у тебя нет доступа(\nНажми \"/change\" чтобы продолжить", reply_markup=markup)
                bot.register_next_step_handler(received_message, change_option)

        elif message.text == 'Узнать расписание':
            sti1 = open('data/stickers/REALLY.webp', 'rb')
            bot.send_sticker(message.chat.id, sti1)
            markup = types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)
            received_message = bot.send_message(
                message.chat.id, "Введи мне номер своей группы, номер недели который тебе нужен и номер дня недели\n\n!!! Format: 6101-010302D 17 5 !!!", reply_markup=markup)
            bot.register_next_step_handler(received_message, send_shedule)

        elif message.text == 'Важные ссылки':
            important_links(message)

        elif message.text == 'News':
            if str(message.from_user.id) == '765103434':
                send_news(message)
            else:
                error(message)
        elif message.text == 'Вернуться в меню':
            change_option(message)

        else:
            error(message)


def error(message) -> None:
    '''
    Функция вывода информации о неверном вводе от пользователя, возвращает в начало
    '''
    sti3 = open('data/stickers/IDK.webp', 'rb')
    bot.send_sticker(message.chat.id, sti3)
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("/start")
    markup.add(item1)
    received_message_text = bot.send_message(
        message.chat.id, 'Блинб, я не знаю, что ответить(((\nНажми \"/start\" чтобы продолжить', reply_markup=markup)
    bot.register_next_step_handler(received_message_text, welcome)


def open_file(way_to_file: str) -> bool:
    '''
    Проверка наличия файла
    '''
    return os.path.exists(way_to_file)


def important_links(message) -> None:
    '''
    Вывод ссылок на сообщества
    '''
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "ИИК Приём - https://vk.com/iik.ssau.priem\nСтуд. совет ИИК - https://vk.com/sciic\nРасписание ИИК - https://ssau.ru/rasp/faculty/492430598?course=1\nSSAU - https://ssau.ru\n", reply_markup=markup)
    print(
        f"Отправлено {message.text} -> Пользователь {message.from_user.first_name} -> ID: {message.from_user.id}")
    change_option(message)


def send_shedule(message) -> None:
    '''
    Отправка расписания, при желании можно запросить вывод расписания сессии
    '''
    if message.text == 'Вернуться в меню':
        change_option(message)
    else:
        if not os.path.isdir('AllGroupShedule'):
            gs.pars_all_group()
        try:
            num_group = message.text.split()[0]
            selectedWeek = message.text.split()[1]
            selectedWeekday = message.text.split()[2]
            url_schedule = gs.find_schedule_url(
                num_group, selectedWeek, selectedWeekday)
            schedule = gs.pars_shedule(url_schedule)
            bot.send_message(
                message.chat.id, schedule + f"\nURL: {url_schedule}")
            with open(f"data/work_with_group_id/{message.chat.id}.txt", "w", encoding="utf-8") as file:
                file.write(num_group)
            print(
                f"Отправлено расписание {message.text} -> Пользователь {message.from_user.first_name} -> ID: {message.from_user.id}")
            markup = types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            item1 = types.KeyboardButton("Узнать расписание сессии")
            item2 = types.KeyboardButton("Вернуться в меню")
            markup.add(item1, item2)
            received_message = bot.send_message(
                message.chat.id, "Хочешь узнать что-то ещё?", reply_markup=markup)
            bot.register_next_step_handler(
                received_message, send_session_shedule)
        except:
            error(message)


def send_session_shedule(message) -> None:
    '''
    Отправка расписания сессии
    '''
    if message.text == "Вернуться в меню":
        os.remove(f"data/work_with_group_id/{message.chat.id}.txt")
        change_option(message)
    else:
        try:
            num_group = ""
            with open(f"data/work_with_group_id/{message.chat.id}.txt", "r", encoding="utf-8") as file:
                num_group = file.read()
            schedule = gs_session.pars_schedule_session(num_group)
            url_schedule = gs_session.find_schedule_session_url(num_group)
            markup = types.ReplyKeyboardRemove()
            bot.send_message(
                message.chat.id, schedule + f"\nURL: {url_schedule}", reply_markup=markup)
            os.remove(f"data/work_with_group_id/{message.chat.id}.txt")
            print(
                f"Отправлено расписание сессии -> Пользователь {message.from_user.first_name} -> ID: {message.from_user.id}")
            change_option(message)
        except:
            bot.send_message(
                message.chat.id, "Возникла ошибка, возможно расписания сессии ещё нет(")


def send_news(message) -> None:
    '''
    Отправка "новостей". Админ отправляет всем пользователям, кто сохранён в базе какую-либо информацию прописанную в файлу info.txt
    '''
    with open('data/info.txt', 'r', encoding="utf-8") as file:
        news = file.read()
    with open('users.csv', 'r', encoding="utf-8") as file:
        readerder = csv.reader(file, delimiter=";")
        for row in readerder:
            try:
                bot.send_message(row[2], news)
                print(f"Отправлены новости пользователю {row[2]}")
            except:
                pass
    change_option(message)


def change_lab_task(message) -> None:
    '''
    Выбор задания лабораторной работы
    '''
    list_items = []
    list_files = []
    if message.text == 'Вернуться в меню':
        change_option(message)
    else:
        try:
            list_files = os.listdir(f"data/labs_book/labs/{message.text}")
            for files in list_files:
                list_items.append(files)
            markup = types.ReplyKeyboardRemove()
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            for item in list_items:
                markup.add(item)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)
            received_message = bot.send_message(
                message.chat.id, "Номер?", reply_markup=markup)
            bot.register_next_step_handler(received_message, send_pdf)
        except:
            error(message)


def change_book(message) -> None:
    '''
    Выбор учебника
    '''
    list_items = []
    list_files = []
    markup = types.ReplyKeyboardRemove()
    if message.text == 'Вернуться в меню':
        change_option(message)
    else:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        try:
            list_files = os.listdir(f"data/labs_book/{message.text}")
            for files in list_files:
                list_items.append(files)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            for item in list_items:
                markup.add(item)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)
            received_message = bot.send_message(
                message.chat.id, "Автор?", reply_markup=markup)
            bot.register_next_step_handler(received_message, send_pdf)
        except:
            error(message)


def change_secret(message) -> None:
    '''
    Выбор секкретного материала (доступно только для определённых пользователей)
    '''
    list_items = []
    for doc in os.listdir("secret"):
        list_items.append(doc)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    for item in list_items:
        markup.add(item)
    item = types.KeyboardButton("Вернуться в меню")
    markup.add(item)
    received_message = bot.send_message(
        message.chat.id, "Какой секретик нужен?", reply_markup=markup)
    bot.register_next_step_handler(received_message, send_secret)


def send_secret(message) -> None:
    '''
    Отправка секретног материала
    '''
    if not message.text == 'Вернуться в меню':
        bot.send_message(message.chat.id, "Отправляю!")
        file = open(f"secret/{message.text}", "rb")
        bot.send_document(message.chat.id, file)
        print(
            f"Отправлен {message.text} -> Пользователь {message.from_user.first_name} -> ID: {message.from_user.id}")
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("/change")
        markup.add(item1)
        received_message = bot.send_message(
            message.chat.id, "Нажми \"/change\" чтобы продолжить", reply_markup=markup)
        bot.register_next_step_handler(received_message, change_option)
    else:
        change_option(message)


def send_pdf(message) -> None:
    '''
    Отправка pdf-файлов пользователю
    '''
    if message.text == 'Вернуться в меню':
        change_option(message)
    else:
        way_to_file = ""
        start_search = True
        while start_search:
            for subject in os.listdir("data/labs_book/"):
                way_to_file = f"data/labs_book/{subject}/{message.text}"
                if open_file(way_to_file):
                    start_search = False
                    break
            if start_search:
                while start_search:
                    for subject in os.listdir("data/labs_book/labs/"):
                        way_to_file = f"data/labs_book/labs/{subject}/{message.text}"
                        if open_file(way_to_file):
                            start_search = False
                            break
        needed_book = open(way_to_file, 'rb')
        bot.send_message(message.chat.id, "Отправляю")
        bot.send_document(message.chat.id, needed_book)
        print(
            f"Отправлен {message.text} -> Пользователь {message.from_user.first_name} -> ID: {message.from_user.id}")
        sti = open('data/stickers/NYA.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("/change")
        markup.add(item1)
        received_message = bot.send_message(
            message.chat.id, "Нажми \"/change\" чтобы продолжить", reply_markup=markup)
        bot.register_next_step_handler(received_message, change_option)


if __name__ == "__main__":
    while True:
        try:
            print("Eddie Start!")
            bot.polling(none_stop=True)
        except:
            print("Some problem, restart")
            time.sleep(15)
