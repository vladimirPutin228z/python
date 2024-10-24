#задание 1
names = ["Richard", "Igor", "Jonathan", "Alice", "Mary", "Bonnie"]
for name in names:
    print("Hello {name}!")
#задание 2
phrase = "I'm learning cycles."
for  in range(10):
    print(phrase)

#Задание 3
stations = ["Малиновка", "Рябиновка", "Суслово", "Дрожжино", "Звягино"]

for i, station in enumerate(stations):
    if i == len(stations) - 1:
        print("Поезд на станции: {station} - Конечная!")
    else:
        print("Поезд на станции: {station}")
# Задание 4
shop = ["Laptop", "Smartphone", "Watch", "Tablet", "Headphones"]

for item in shop:
    if item == "Laptop":
        print("I'm buying this.")
    else:
        print("I don't need it.")
# Задание 5
tasks = ["Сдать проект (Важная)", "Сходить в магазин", "Позвонить врачу (Важная)", "Убраться в комнате", "Подготовить отчёт"]

for i, task in enumerate(tasks, 1):
    if "Важная" in task:
        print("{i}! {task}")
    else:
        print("{i}. {task}")
# Задание 6
x = int(input("Сколько чисел вы хотите ввести? "))
numbers = []
total = 0

for  in range(x):
    num = int(input("Введите число: "))
    numbers.append(num)
    total += num

print("Список всех введённых чисел: {numbers}")
print("Сумма всех чисел: {total}")
# Задание 7
x = 0

while x < 10:
    x += 1
    print("Итерация: {counter}")
# Задание 8
while True:
    command = input("Введите команду: ")

    if command == "w":
        print("Персонаж идёт вперёд.")
    elif command == "a":
        print("Персонаж идёт влево.")
    elif command == "s":
        print("Персонаж идёт назад.")
    elif command == "d":
        print("Персонаж идёт вправо.")
    elif command == "stop":
        print("Программа завершена.")
        break
    else:
        print("Неизвестная команда! Попробуйте снова.")
# Задание 9
while True:
    num = int(input("Введите число от 1 до 9: "))
    
    if 1 <= num <= 9:
        for i in range(1, 11):
            print("num * i ")
        break
    else:
        print("Число вне диапазона. Пожалуйста, попробуйте снова.")
# Задание 10
correct_answer = "солнце"
attempts = 3

while attempts > 0:
    answer = input("Загадка: Что всегда светит на небе? ").
    
    if answer == correct_answer:
        print("Правильно! Вы угадали.")
        break
    else:
        attempts -= 1
        if attempts > 0:
            print("Неправильно. Осталось попыток: {attempts}.")
        else:
            print("Вы исчерпали все попытки. Ответ был: солнце.")
    
    
    
