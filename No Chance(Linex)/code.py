import json
import time
import os.path
import pygame
import os
from sys import platform


# Отчищает вывод
def clean2dot0():
    if platform == "win32" or platform == "cygwin":
        os.system('cls')
    else:
        os.system('clear')


# Отвечает за музыку в игре
def music(n):
    namefile = "music\\" + n + '.mp3'
    pygame.mixer.music.load(namefile)
    pygame.mixer.music.play(-1)


# Функция команды "Авто прохождение" отвечающая за хождению по псевдо-графу.
def checer2(pos, data):
    if data[pos[0] - 1][pos[1]] != '0':
        return data[pos[0] - 1][pos[1]]
    elif data[pos[0]][pos[1] - 1] != '0':
        return data[pos[0]][pos[1] - 1]
    else:
        return data[pos[0]][pos[1] + 1]


# Функция команды "Авто прохождение"
def AutoP(number, data):
    a = data
    maze = [
        ['0', '0', '2.3', '0', '0'],
        ['0', '0', '2.2', '0', '0'],
        ['0', '0', '2', '0', '0'],
        ['0', '3', '1', '4', '0'],
        ['0', '0', '*', '4.1', '0'],
        ['0', '0', '*', '0', '0'],
        ['0', '0', '*', '*', '0'],
        ['0', '0', '5', '5.2', '0']
        ]

    dictMaze = {
        "2.3": [0, 2],
        '2.2': [1, 2],
        '2': [2, 2],
        '1': [3, 2],
        '3': [3, 1],
        '4': [3, 3],
        '5': [7, 2],
        '4.1': [4, 3],
        '5.2': [7, 3]
    }

    if number in dictMaze:
        pleas = dictMaze[number]
        maze2 = maze[pleas[0]][pleas[1]]
        Fpleas = dictMaze[checer2(pleas, maze)]
        Fdf = maze[Fpleas[0]][Fpleas[1]]
        print(a[maze2]["way"].index(Fdf) + 1)
        while True:
            if pleas == [0, 2]:
                return "end"
            elif maze[pleas[0]][pleas[1] + 1] == '*' or maze[pleas[0]][pleas[1] - 1] == '*'\
                    or maze[pleas[0] - 1][pleas[1]] == '*':
                pleas = [3, 2]
            else:
                pleas = dictMaze[checer2(pleas, maze)]
            maze2 = maze[pleas[0]][pleas[1]]
            print(a[maze2]["text"])
            music(maze2)
            time.sleep(6)
            if a[maze2]["way"] != ["end"]:
                Fpleas = dictMaze[checer2(pleas, maze)]
                Fdf = maze[Fpleas[0]][Fpleas[1]]
                print(a[maze2]["way"].index(Fdf) + 1)

    else:
        print("Запрос отклонен.")
        print('Иногда надо и самому подумать, и это тот самый момент.')
        return 'rep'


# Функция команды "Продолжить"
def Continue1():
    return 'rep'


# Функция команды "Начать с насала"
def BStart():
    return 33


# Функция модерирующая команды
def Comands(number, data):

    print('Список команд:')
    print('1. Продолжить игру')
    print('2. Начать с начала')
    print('3. Авто прохождение')
    print('Введите номер команды')
    flag = True
    comands = ['Continue1()', 'BStart()', 'AutoP(number, data)']
    while flag:
        ans = input()
        if ans == "!":
            print('Вы ввели некорректное значение, попробуйте ещё раз.')
            continue
        ans = checer(ans)
        if type(ans) == int:
            flag = False
        else:
            print('Вы ввели некорректное значение, попробуйте ещё раз.')
    return eval(comands[ans - 1])


# авто сахронение
def AutoSave(n):
    with open("savePoint.json", 'w') as AutoSaveF:
        AutoSaveF.seek(0)
        json.dump([n], AutoSaveF)


# проверяет вводимые данные.
def checer(prob, data={"0": {"way": [1, 2, 3]}}, num="0"):
    if prob.isdigit() or prob.replace('.', '', 1).isdigit():
        if int(prob) >= 1 and int(prob) <= len(data[num]["way"]):
            return int(prob)
    elif prob == '!':
        return Comands(num, data)
    else:
        return "error"


# сама игра.
def turn(data, num):  # отвечает за вывод и принятие данных.

    print(data[num]["text"])
    if data[num]["way"][0] != "end":
        flag = True
        a = input()
        while flag:
            answer = checer(a, data, num)
            if type(answer) == int:
                flag = False
            elif answer == 'rep':
                print('Вводите:')
                a = input()
                continue
            elif answer == 'end':
                return 'end'
            else:
                print('Вы ввели некорректное значение, попробуйте ещё раз.')
                a = input()
        return data[num]["way"][answer - 1] if answer != 33 else '1'
    else:
        print("Не получилось досмотреть сон до конца, не судьба.")  # конец игры
        return 'end'





pygame.init()

with open('story.json', encoding='utf-8') as file:
    print('Это игра, текстовый квест, под названием "No Chance", правила не сложные:')
    print('1.Читаешь текст и выбираешь цифры действий, вернуться домой')
    print('2.Ещё есть пару команд, их список можно увидеть введя "!".\nПриятной игры')
    storyDict = json.load(file)

if os.path.exists('savePoint.json') is False:
    with open('savePoint.json', 'w+') as file1:
        json.dump(["1"], file1)
with open('savePoint.json') as f:
    step = json.load(f)[0]

while True: # цикал игры.

    music(step)

    step = turn(storyDict, step)
    clean2dot0()
    AutoSave(step)
    if step == "end":
        AutoSave('1')
        time.sleep(17)
        music("end")
        time.sleep(4)
        if input('Введите "new game" чтобы начать игру заново') == "new game":
            step = '1'
        else:
            break

