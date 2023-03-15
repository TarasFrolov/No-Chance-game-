import json
import time


def checer2(pos, data):
    if data[pos[0] - 1][pos[1]] != '0':
        return data[pos[0] - 1][pos[1]]
    elif data[pos[0]][pos[1] - 1] != '0':
        return data[pos[0]][pos[1] - 1]
    else:
        return data[pos[0]][pos[1] + 1]

def AutoP(number, data):
    a = data
    maze = [
        ['0', '0', '2.1', '0', '0'],
        ['0', '0', '1.1', '0', '0'],
        ['0', '0', '2', '0', '0'],
        ['0', '3', '1', '4', '0'],
        ['0', '0', '*', '1.4', '0'],
        ['0', '0', '*', '0', '0'],
        ['0', '0', '*', '*', '0'],
        ['0', '0', '5', '2.5', '0']
        ]

    dictMaze = {
        "2.1": [0, 2],
        '1.1': [1, 2],
        '2': [2, 2],
        '1': [3, 2],
        '3': [3, 1],
        '4': [3, 3],
        '5': [7, 2],
        '1.4': [4, 3],
        '2.5': [7, 3]
    }

    if number in dictMaze:
        pleas = dictMaze[number]
        df = maze[pleas[0]][pleas[1]]
        Fpleas = dictMaze[checer2(pleas, maze)]
        Fdf = maze[Fpleas[0]][Fpleas[1]]
        print(a[df]["way"].index(Fdf) + 1)
        while True:
            if pleas == [0, 2]:
                return "end"
            elif maze[pleas[0]][pleas[1] + 1] == '*' or maze[pleas[0]][pleas[1] - 1] == '*'\
                    or maze[pleas[0] - 1][pleas[1]] == '*':
                pleas = [3, 2]
            else:
                pleas = dictMaze[checer2(pleas, maze)]
            df = maze[pleas[0]][pleas[1]]
            print(a[df]["text"])
            time.sleep(6)
            if a[df]["way"] != ["end"]:
                Fpleas = dictMaze[checer2(pleas, maze)]
                Fdf = maze[Fpleas[0]][Fpleas[1]]
                print(a[df]["way"].index(Fdf) + 1)

    else:
        print("Запрос откланен.")
        print('Иногда надо и самому подумать, и это тот самый момент.')
        return 'rep'



def Continue1(number, data, a):
    return 'rep'


def BStart():
    return 33


def Comands(number, data, a):

    print('Список команд:')
    print('1. Продолжить игру')
    print('2. Начать с начала')
    print('3. Авто прохождение')
    print('Видите номер команды')
    flag = True
    comands = ['Continue1(number, data, a)', 'BStart()', 'AutoP(number, data)']
    while flag:
        ans = input()
        if ans == "!":
            print('Вы ввели не коректное значение, поробуйте ещё раз.')
            continue
        ans = checer(ans)
        if type(ans) == int:
            flag = False
        else:
            print('Вы ввели не коректное значение, поробуйте ещё раз.')
    return eval(comands[ans - 1])


# авто сахронение
def AutoSave(n):
    with open("savePoint.json", 'w') as AutoSaveF:
        AutoSaveF.seek(0)
        json.dump([n], AutoSaveF)


# проверяет вводимые данные.
def checer(prob, data={"0": {"way": [1, 2, 3]}}, num="0"):
    if prob.isdigit() or prob.replace('.', '', 1).isdigit():
        if int(prob) >= 1 or int(prob) <= len(data[num]["way"]):
            return int(prob)
    elif prob == '!':
        return Comands(num, data, prob)
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
                print('Вы ввели не коректное значение, поробуйте ещё раз.')
                a = input()
            return data[num]["way"][answer - 1] if answer != 33 else '1'
    else:
        print("Не получилось досмотреть сон до конца, не судьба.")  # конец игры
        return 'end'






with open('story.json', encoding='utf-8') as file:
    print('Это игра, текстовый квест, под названием "No Chance", правила не сложные:')
    print('1.Читаешь текст и выбираешь цифры действий, задача проснуться(желательно безболезненно)')
    print('2.Ещё есть пару каманд, их списак можно увидеть введя "!".\nПриятной игры')
    storyDict = json.load(file)

with open('savePoint.json') as file1:
    step = json.load(file1)[0]

while True: # цикал игры.
    step = turn(storyDict, step)
    AutoSave(step)
    if step == "end":
        AutoSave('1')
        if input('Ввидите "new game" чтобы начать игру занова') == "new game":
            step = '1'
        else:
            break
