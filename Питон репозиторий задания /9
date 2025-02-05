#задание 1
class Create_Personage:
    def __init__(self, name_pers, class_pers, hp_pers, damage_pers):
        self.name_pers = name_pers
        self.class_pers = class_pers
        self.hp_pers = hp_pers
        self.damage_pers = damage_pers

    def print_info(self):
        print("Имя:", self.name_pers)
        print("Класс:", self.class_pers)
        print("Жизни:", self.hp_pers)
        print("Урон:", self.damage_pers)
        print()

    def go_on_a_trip(self):
        print(f"Персонаж {self.name_pers} отправился в путешествие и пока недоступен.")
        print()

    def go_back(self):
        print(f"Персонаж {self.name_pers} возвращается назад.")
        print()

    def start_training(self):
        print(f"Персонаж {self.name_pers} начал тренировку. Некоторое время он не будет доступен, однако станет сильнее!")
        self.damage_pers += 5
        self.hp_pers += 3
        print()

    def start_the_battle(self):
        print(f"Персонаж {self.name_pers} хочет начать сражаться!")
        print(f"Его показатели: Жизни: {self.hp_pers} и урон: {self.damage_pers}")
        print()


pers_1 = Create_Personage("Вадим", "воин", 83, 22)
pers_1.print_info()
pers_1.go_on_a_trip()
pers_1.go_back()
pers_1.start_training()
pers_1.print_info()
pers_1.start_the_battle()




#ЗАДАНИЕ 2
class Room:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.is_locked_status = False
        self.theme = None

    def add_item(self, *args):
        if not self.is_locked_status:
            self.items.extend(args)
        else:
            print(f"Ошибка: Комната {self.name} заблокирована. Невозможно добавить предметы.")

    def print_items(self):
        print(f"Все предметы в комнате {self.name}: {', '.join(self.items)}")

    def del_item(self, item):
        if not self.is_locked_status:
            if item in self.items:
                self.items.remove(item)
                print(f"Предмет {item} удален из комнаты {self.name}.")
            else:
                print(f"Предмет {item} не найден в комнате {self.name}.")
        else:
            print(f"Ошибка: Комната {self.name} заблокирована. Невозможно удалить предметы.")

    def find_item(self, item):
        if item in self.items:
            print(f"Предмет {item} находится в комнате {self.name}.")
            return True
        else:
            print(f"Предмет {item} не найден в комнате {self.name}.")
            return False

    def rename_room(self, new_name):
        print(f"Комната {self.name} переименована в {new_name}.")
        self.name = new_name

    def lock_room(self):
        self.is_locked_status = True
        print(f"Комната {self.name} заблокирована.")

    def get_items_starting_with(self, letter):
        starting_items = [item for item in self.items if item.startswith(letter)]
        print(f"Предметы в комнате {self.name}, начинающиеся с буквы '{letter}': {', '.join(starting_items)}")
        return starting_items

    def count_specific_item(self, item):
        count = self.items.count(item)
        print(f"Предмет '{item}' встречается в комнате {self.name} {count} раз(а).")
        return count

    def set_theme(self, theme):
        self.theme = theme
        print(f"Для комнаты {self.name} установлена тема: {theme}")

    def show_theme(self):
        if self.theme:
            print(f"Тема комнаты {self.name}: {self.theme}")
        else:
            print(f"Для комнаты {self.name} тема не установлена.")


room1 = Room("Кухня")
room2 = Room("Спальня")


room1.add_item("Холодильник", "Стул", "Стол")
room2.add_item("Кровать", "Тумбочка", "Шкаф")


room1.find_item("Стул")
room1.find_item("Ковер")

room1.rename_room("Столовая")
room1.print_items()

room2.show_theme()
room1.show_theme()

#задание 3
def isint(var):
    if type(var) == type(1):
        return True
    else:
        return False


class Book:
    def __init__(self, name: str, pages: int, year: int):
        self.name = name
        self.pages = pages
        self.year = year

    def info(self):
        print(f"Название: {self.name}\nКоличество страниц: {self.pages}\nГод издания: {self.year}\n")

    def update_pages(self, pages: int):
        if isint(pages):
            self.pages = pages
        else:
            print("Неверное значение страниц\n")

    def older_than(self, year: int):
        if isint(year):
            if self.year > year:
                print(True)
            else:
                print(False)
        else:
            print("Неверное значение года\n")


book1 = Book("Name1", 200, 2005)
book2 = Book("Name2", 500, 1999)
book1.info()
book1.update_pages(250)
book1.info()
book2.older_than(2000)
