import re
from function import *
arr_tree = Tree_list()
names = []

def find_words(line):
    #ділимо за пробілами рядок на слова
    arr_words = re.findall(r'\w+', line)
    #шукаємо
    name = arr_words[1]
    if re.match(r'^[Cc][Rr][Ee][Aa][Tt][Ee]\b', arr_words[0]):
        create(arr_words)
    elif re.match(r'^[Ii][Nn][Ss][Ee][Rr][Tt]\b', arr_words[0]):
        insert(arr_words, line, arr_tree[name].size)
    elif re.match(r'^[Pp][Rr][Ii][Nn][Tt][_][Tt][Rr][Ee][Ee]\b', arr_words[0]):
        print_tree(arr_words)
    elif re.match(r'^[Cc][Oo][Nn][Tt][Aa][Ii][Nn][Ss]\b', arr_words[0]):
        contains(arr_words, line)
    elif re.match(r'^[Ss][Ee][Aa][Rr][Cc][Hh]\b', arr_words[0]):
        search(arr_words, line)
    else:
        print("Неправильна назва команди або назва команди відсутня взагалі\n")

def create(arr_words):
    name = arr_words[1]
    if (len(arr_words) == 2):
        if (name in names):
            print("Множина", name, "не була створена, бо вже існує множина з таким іменем\n")
            print(names)
        else:
            names.append(name)
            arr_tree[name] = []
            print("Множина", name, "була створена\n")
    else:
        print("Неправильно введена команда 'CREATE'\n")

def insert(arr_words, line, size):
    k = 0
    m = 0
    temp1 = []
    temp2 = []
    #дістаємо ім'я множини
    name = arr_words[1]
    #перевіряємо наявність цієї множини (співпадіння назви з одним із елементів масиву)
    if (name in names):
        #перевіряємо правильність команди і дістаємо значення x та у
        a = re.split(r'[(]', line)
        N = re.findall(r'\w+', a[0])
        if (len(N) == 2):
            b = re.split(r'[)]', a[1])
            c = re.findall(r'\S', b[0])
            for i in range(len(c)):
                if (c[i] == ','):
                    k = i
            for j in range(0, k):
                temp1.append(c[j])
            for l in range(k + 1,len(c)):
                temp2.append(c[l])
            if(len(temp1) > 1):
                x = int(''.join(temp1))
            else:
                x = int(temp1[0])
            if(len(temp2) > 1):
                y = int(''.join(temp2))
            else:
                y = int(temp2[0])
            #записуємо х та у
            if (size == 0):
                arr_tree[name].add([x, y])
                print(f"Точка ( {x},{y} ) була додана до {name}")
            elif(arr_tree[name].contains(arr_tree[name].root, [x,y]) == True):
                print("Елемент був вже доданий")
            else:
                arr_tree[name].add([x, y])
                print(f"Точка ( {x},{y} ) була додана до {name}")
        else:
            print("Неправильно введена команда 'INSERT'\n")
    else:
        print("Точка не була додана до", name, ", бо множина з таким іменем не існує\n")

def print_tree(arr_words):
    #дістаємо ім'я множини
    name = arr_words[1]
    #перевіряємо правильність команди
    if (len(arr_words) == 2):
        #перевіряємо наявність цієї множини (співпадіння назви з одним із елементів масиву)
        if (name not in names):
            print("Внутрішня структура KD-дерева, побудованого для множини", name, "не була виведена, бо множина з таким іменем не існує\n")
            print(names)
        else:
            print("Внутрішня структура KD-дерева, побудованого для множини", name, "\n")
            for i in range(len(arr_tree)):
                if (arr_tree[i][0] == name):
                    print(arr_tree[i])
            #тут буде функція виведення структури дерева
    else:
        print("Неправильно введена команда 'PRINT_TREE'\n")

def contains(arr_words, line):
    k = 0
    m = 0
    w = 0
    temp1 = []
    temp2 = []
    #дістаємо ім'я множини
    name = arr_words[1]
    #перевіряємо наявність цієї множини (співпадіння назви з одним із елементів масиву)
    if (name in names):
        #перевіряємо правильність команди і дістаємо значення x та у
        a = re.split(r'[(]', line)

        N = re.findall(r'\w+', a[0])
        if (len(N) == 2):
            b = re.split(r'[)]', a[1])
            c = re.findall(r'\S', b[0])
            for i in range(len(c)):
                if (c[i] == ','):
                    k = i
            for j in range(0, k):
                temp1.append(c[j])
            for l in range(k + 1,len(c)):
                temp2.append(c[l])
            if(len(temp1) > 1):
                x = int(''.join(temp1))
            else:
                x = int(temp1[0])
            if(len(temp2) > 1):
                y = int(''.join(temp2))
            else:
                y = int(temp2[0])
            #шукаємо х та у
            print(arr_tree[name].contains(arr_tree[name].root, [x,y]))
        else:
            print("Неправильно введена команда 'CONTAINS'\n")
    else:
        print("Точка не була додана до", name + ", бо множина з таким іменем не існує\n")

def search(arr_words, line):
    k = 0
    m = 0
    n = 0
    temp1 = []
    temp2 = []
    temp11 = []
    temp12 = []
    #дістаємо ім'я множини
    name = arr_words[1]
    #перевіряємо правильність команди
    if (len(arr_words) == 2):
        #перевіряємо наявність цієї множини (співпадіння назви з одним із елементів масиву)
        if (name not in names):
            print("Всі точки із множини", name, "не були виведені, бо множина з таким іменем не існує\n")
            print(names)
        else:
            print("Всі точки із множини", name, "будуть виведені:")
            arr_tree[name].recursive_search(arr_tree[name].root)
    #перевіряємо правильність команди WHERE
    elif re.match(r'^[Ww][Hh][Ee][Rr][Ee]\b', arr_words[2]):
        if (len(arr_words) == 5):
            #дістаємо значення y
            y = int(arr_words[4])
            #перевіряємо правильність команди ABOVE_TO
            if re.match(r'^[Aa][Bb][Oo][Vv][Ee][_][Tt][Oo]\b', arr_words[3]):
                #перевіряємо наявність цієї множини (співпадіння назви з одним із елементів масиву)
                if (name not in names):
                    print("Пошук точок у множині", name, "не був проведений, бо множина з таким іменем не існує\n")
                    print(names)
                else:
                    print("Всі точки із множини", name, "координата y, яких більша за", y, "будуть виведені\n")
                    for i in range(len(arr_tree)):
                        if (arr_tree[i][0] == name):
                            k = i
                    for j in range(1, len(arr_tree[k])):
                        if (arr_tree[k][j][1] > y):
                            print("(" + str(arr_tree[k][j][0]) + ",", str(arr_tree[k][j][1]) + ")")
            else:
                print("Неправильно введена команда 'ABOVE_TO'")
        #перевіряємо правильність команди NN
        elif re.match(r'^[Nn][Nn]\b', arr_words[3]):
            #перевіряємо правильність команди і дістаємо значення x та у
            a = re.split(r'[(]', line)
            N = re.findall(r'\w+', a[0])
            if (len(N) == 4):
                b = re.split(r'[)]', a[1])
                c = re.findall(r'\S', b[0])
                for i in range(len(c)):
                    if (c[i] == ','):
                        k = i
                for j in range(0, k):
                    temp1.append(c[j])
                for l in range(k + 1,len(c)):
                    temp2.append(c[l])
                if(len(temp1) > 1):
                    x = int(''.join(temp1))
                else:
                    x = int(temp1[0])
                if(len(temp2) > 1):
                    y = int(''.join(temp2))
                else:
                    y = int(temp2[0])
                #тут буде функція пошуку найближчого сусіда
                print("Найближчий сусід точки (" + str(x) + ",", str(y) + ") точка ...\n")
            else:
                print("Неправильно введена команда 'NN'\n")
        #перевіряємо правильність команди INSIDE
        elif re.match(r'^[Ii][Nn][Ss][Ii][Dd][Ee]\b', arr_words[3]):
            #перевіряємо правильність команди і дістаємо значення x та у
            a = re.split(r'[(]', line)
            N = re.findall(r'\w+', a[0])
            if (len(N) == 4):
                b = re.split(r'[)]', a[1])
                c = re.findall(r'\S', b[0])
                d = re.findall(r'\S', b[1])
                e = re.split(r'[)]', a[2])
                f = re.findall(r'\S', b[0])
                #перевіряємо наявність коми між точками
                if (d[0] == ','):
                    #дістаємо значення x та у нижнього лівого кута
                    for i in range(len(c)):
                        if (c[i] == ','):
                            k = i
                    for j in range(0, k):
                        temp1.append(c[j])
                    for l in range(k + 1,len(c)):
                        temp2.append(c[l])
                    if(len(temp1) > 1):
                        x1 = int(''.join(temp1))
                    else:
                        x1 = int(temp1[0])
                    if(len(temp2) > 1):
                        y1 = int(''.join(temp2))
                    else:
                        y1 = int(temp2[0])
                    #дістаємо значення x та у верхнього правого кута
                    for i in range(len(f)):
                        if (f[i] == ','):
                            n = i
                    for j in range(0, n):
                        temp11.append(f[j])
                    for l in range(n + 1,len(f)):
                        temp12.append(f[l])
                    if(len(temp11) > 1):
                        x2 = int(''.join(temp11))
                    else:
                        x2 = int(temp11[0])
                    if(len(temp12) > 1):
                        y2 = int(''.join(temp12))
                    else:
                        y2 = int(temp12[0])
                    #тут буде функція пошуку точок у прямокутнику
                    print("Точки, які містяться всередині або лежать на сторонах прямокутника, який задано координатами його вершин: (" + str(x1) + ",", str(y1) + ") - координати нижнього лівого кута, (" + str(x2) + ",", str(y2) + ") - координати верхнього правого кута: ...\n")
                else:
                    print("Неправильно введена команда 'INSIDE'\n")
            else:
                print("Неправильно введена команда 'INSIDE'\n")
        else:
            print ("Неправильно введена команда 'SEARCH'\n")
    else:
        print ("Неправильно введена команда 'SEARCH'\n")

str = ''
while True:
    str += ' ' + input("-->").strip()
    if ';' in str:
    	for command in str.split(';'):
            if command:
                command = command.strip()
                try:
                  find_words(command)
                except:
                  print("Ви допустили помилку ")
                str = ''