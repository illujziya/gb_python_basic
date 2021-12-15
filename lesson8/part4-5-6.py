# 4. Начните работу над проектом «Склад оргтехники». 
# Создайте класс, описывающий склад. 
# А также класс «Оргтехника», который будет базовым для классов-наследников. 
# Эти классы — конкретные типы оргтехники (принтер, сканер, ксерокс). 
# В базовом классе определить параметры, общие для приведенных типов. 
# В классах-наследниках реализовать параметры, уникальные для каждого типа оргтехники.

# 5. Продолжить работу над первым заданием. 
# Разработать методы, отвечающие за приём оргтехники на склад и передачу в определенное подразделение компании. 
# Для хранения данных о наименовании и количестве единиц оргтехники, а также других данных, можно использовать любую подходящую структуру, например словарь.

# 6. Продолжить работу над вторым заданием. Реализуйте механизм валидации вводимых пользователем данных. 
# Например, для указания количества принтеров, отправленных на склад, нельзя использовать строковый тип данных.
# Подсказка: постарайтесь по возможности реализовать в проекте «Склад оргтехники» максимум возможностей, изученных на уроках по ООП.

from abc import ABC, abstractmethod
from random import randint

# Справочные типы для параметров техники
class PaperFormat:
    """Максимальный формат бумаги"""
    class A0: pass
    class A1: pass
    class A2: pass
    class A3: pass
    class A4: pass

class PrintingType:
    """Тип печати"""
    class Laser: """Лазерная печать"""
    class Ink: """Струйная печать"""
    class BW: """Черно-белая печать"""
    class Color: """Цветная печать"""

class Connectivity:
    """Возможность подключения"""
    class USB: pass
    class Wifi: """Беспроводное подключение (Wifi)"""
    class Etherhet: """Локальная сеть (Ethernet)"""
    class AirPrint: """Поддержка технологии AirPrint"""


class ScanResolution:
    """Разрешение сканирования"""
    class DPI600:  """600x600 DPI"""
    class DPI1200: """1200x1200 DPI"""
    class DPI6400: """6400x9600 DPi"""

class ScannerType:
    """Тип сканера"""
    class EdgeFed: """протяжный""" #какое странное слово для сканера :)
    class FlatBed: """планшетный"""


class Spec():
    """ Всякие методы для работы со справочными типами """
    @staticmethod
    def get_human_name(cls):
        """ возвращает описание типа или его имя (если описания нет)"""
        return cls.__doc__ if cls.__doc__ is not None else cls.__name__ 

    @staticmethod
    def get_fullname(cls):
        """ возвращает полное имя, например: PaperFormat.A1 """
        return cls.__qualname__

    @staticmethod
    def get_parent(cls):
        """ возвращает категорию (родительский тип) """
        return cls.__qualname__.rsplit(".",1)[0]

    @staticmethod
    def get_as_string(cls):
        """ возвращает строку с перечислением всех подтипов если они есть"""
        result = f"{Spec.get_human_name(cls)}: "
        variants = []
        for item in cls.__dict__.values():
            if isinstance(item, type):                
                variants.append(Spec.get_fullname(item))
        return result + ", ".join(variants)
                

class Warehouse:
    """ Склад """
    items: dict
    name: str

    def __init__(self, name):
        self.items = {}
        self.name = name

    def add(self,item,quantity):
        """ прием оборудования на склад. (оборудование,количество)"""
        if item not in self.items:
            self.items[item] = quantity
        else:
            self.items[item] += quantity
        print(f"{self.name}: принято оборудование { item.type } { item.model }, в количестве { quantity } шт.")

    def __str__(self):
        """ возвращает список позиций на складе """
        result = [f"\n{self.name}, перечень оборудования:"]
        for item, quantity in self.items.items():
            result.append(f"\t{ item.type } { item.model } - { quantity } шт.")
        return "\n".join(result)
    
    def find_by_specs(self,*specs):
        """ поиск на складе по параметрам (параметры...) = { оборудование: количество } """
        result = {}
        search_params = []
        for spec in specs:
            # принимает как строки так и классы (не те что в одноклассниках)
            search_params.append(spec if type(spec) is str else Spec.get_fullname(spec))
        
        for item in self.items:
            item_params = [Spec.get_fullname(x) for x in item.specs]
            if all(spec in item_params for spec in search_params):
                result[item] = self.items[item]
        
        return result
    
    def transfer(self,item,quantity,target):
        """ 
        передача оборудования на другой склад\офис 
        (оборудование, количество, получатель)
        """
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError()
        except:
            print("Количество оборудования должно быть челым положительным числом")
            return False

        if item not in self.items:
            print(f"На складе нет оборудования {item.type} {item.model}")
            return False
        
        if self.items[item] < quantity:
            print(f"На складе нет необходимого количества: доступно {self.items[item]}, необходимо {quantity}")
            return False

        self.items[item] -= quantity
        print(f"{self.name}, выдано оборудование: {item.type} {item.model} - {quantity} шт. Осталось на складе: {self.items[item]} шт.")
        # если после передачи количество 0 - убираем со склада
        if self.items[item] == 0: del self.items[item]        
        target.add(item,quantity)

        return True

        
class WarehouseItem(ABC):    
    """ родительский класс для офисной техники """
    _valid_specs = [] # параметры применимые к оборудованию
    specs: list
    model: str        
    type: str
        
    def __init__(self, model, *specs):
        self.model = model        
        # применяем дополнительные параметры только из перечня разрешенных для класса
        valid_spec_names = [Spec.get_parent(x) for x in self._valid_specs]        
        self.specs = []
        for spec in specs:
            if Spec.get_parent(spec) in valid_spec_names: self.specs.append(spec)

    def __str__(self):
        """ выводит полную информацию включая все параметры """
        result = [f"\nИнформация об оборудовании: {self.type }, модель {self.model}"]
        
        # собираем названия категорий
        category_names = {Spec.get_parent(x): Spec.get_human_name(x) for x in self._valid_specs}
        grouped_specs = {}

        # формируем словарь кагория -> параметры (в каждой может быть несколько)
        for spec in self.specs:
            category = Spec.get_parent(spec)
            name = Spec.get_human_name(spec)
            if category not in grouped_specs: grouped_specs[category] = []
            grouped_specs[category].append(name)

        # преобразуем в строку
        for cat in grouped_specs.keys():
            result.append(f"\t{category_names[cat]}:")
            result.append(f"\t\t{', '.join(grouped_specs[cat])}")

        return "\n".join(result)
        

class Printer(WarehouseItem):
    """ тип оборудования - принтер """
    type = "Принтер"
    _valid_specs = [PaperFormat, PrintingType, Connectivity]

class Scanner(WarehouseItem):
    """ тип оборудования - сканер """
    type = "Сканер"
    _valid_specs = [PaperFormat, ScanResolution, Connectivity, ScannerType]

class Copier(WarehouseItem):
    """ тип оборудования - МФУ. в задании это копир но по факту скорее мфу """
    type = "МФУ"
    _valid_specs = [PaperFormat, PrintingType, ScanResolution, Connectivity, ScannerType]


class UserInterface():
    """ пользовательский интерфейс для работы со складами """

    _main_menu = "Работа со складом, доступные операции:\n"\
        "  [1] - Поиск оборудования по характеристикам на складе №1\n"\
        "  [2] - Передача оборудования из склада №1 на склад №2\n"\
        "  [3] - Показать содержимое складов\n"\
        "  [4] - Выход\n"\
        "Введите номер действия: "\

    def __init__(self,warehouse1,warehouse2):
        self._w1 = warehouse1
        self._w2 = warehouse2
        self.run()

    def run(self):
        """ главное меню """
        while (user_input:=input(self._main_menu)) != '4':
            if user_input == '1':
                self.search()
            elif user_input == '2':
                self.transfer()
            elif user_input == '3':
                self.show()
            else:
                print("Неизвестная команда.")

    def search(self):
        """ поиск оборудования """
        print("Поиск оборудования на складе №1")
        print("Доступные параметры:")
        for spec in [PaperFormat,PrintingType,Connectivity,ScanResolution,ScannerType]:
            print("\t",Spec.get_as_string(spec))
        search = input("Введите параметры через пробел или пустую строку для выхода: ").split(" ")
        if not search:            
            return
        
        results = self._w1.find_by_specs(*search)
        if not results:
            print("Ничего не найдено :(")
            return
        
        print("Результаты поиска:")        
        for item, quantity in results.items():
            print(item)
            print("Количество на складе:", quantity)

        print()

    def transfer(self):
        """ передача оборудования """
        print("Передача оборудования со склада №1 на склад №2")
        print("Позиции доступные для передачи:")
        items = list(self._w1.items.keys())
        for i, item in enumerate(items):
            print(f"\t[{i}] {item.type} {item.model} - {self._w1.items[item]} шт.")

        try:
            item_number = int(input("Введите номер позиции: "))
            item_quantity = int(input("Введите количество: "))
            self._w1.transfer(items[item_number],item_quantity, self._w2)
        except IndexError:
            print("Ошибка ввода - неверное указание позиции.")
        except ValueError:
            print("Ошибка ввода - допустимо вводить только числа.")
        except Exception as ex:
            print("Ошибка - ",ex)

    def show(self):
        """ содержимое складов """
        print("Содержимое складов:")
        print(self._w1)
        print(self._w2)
        print()

        

# создаем офисную технику с разными параметрами
office_tech = [
    Printer("Xerox Phaser 3020BI",
            PaperFormat.A4,
            PrintingType.Laser,
            PrintingType.BW,
            Connectivity.USB,
            Connectivity.Etherhet,
            Connectivity.AirPrint),
    Printer("HP DesignJet T230 (24-дюймовый)",
            PaperFormat.A1,
            PrintingType.Ink,
            PrintingType.Color,
            Connectivity.Wifi,
            Connectivity.Etherhet,
            Connectivity.USB),
    Scanner("Brother ADS-3600W",
            PaperFormat.A4,
            ScanResolution.DPI600,
            Connectivity.USB,
            Connectivity.Etherhet,
            ScannerType.EdgeFed),
    Scanner("Mustek A3 1200S",
            PaperFormat.A3,
            ScanResolution.DPI1200,
            Connectivity.USB,            
            ScannerType.FlatBed),
    Copier("Canon PIXMA G3411",
            PaperFormat.A4,
            PrintingType.Ink,
            PrintingType.Color,
            ScanResolution.DPI1200,
            Connectivity.USB,
            Connectivity.Wifi,            
            ScannerType.FlatBed),
    Copier("HP Laser MFP 135a",
            PaperFormat.A4,
            PrintingType.Laser,
            PrintingType.BW,
            ScanResolution.DPI600,
            Connectivity.USB,            
            ScannerType.FlatBed)
]

print("Наполняем склад!")
warehouse = Warehouse("Склад №1")
warehouse2 = Warehouse("Склад №2")
for item in office_tech:
    warehouse.add(item,randint(1,10))

# поехали!
UserInterface(warehouse,warehouse2)

# Результат запуска программы:
# Наполняем склад!
# Склад №1: принято оборудование Принтер Xerox Phaser 3020BI, в количестве 1 шт.
# Склад №1: принято оборудование Принтер HP DesignJet T230 (24-дюймовый), в количестве 4 шт.
# Склад №1: принято оборудование Сканер Brother ADS-3600W, в количестве 9 шт.
# Склад №1: принято оборудование Сканер Mustek A3 1200S, в количестве 3 шт.
# Склад №1: принято оборудование МФУ Canon PIXMA G3411, в количестве 10 шт.
# Склад №1: принято оборудование МФУ HP Laser MFP 135a, в количестве 9 шт.
# Работа со складом, доступные операции:
#   [1] - Поиск оборудования по характеристикам на складе №1
#   [2] - Передача оборудования из склада №1 на склад №2
#   [3] - Показать содержимое складов
#   [4] - Выход
# Введите номер действия: 1
# Поиск оборудования на складе №1
# Доступные параметры:
#          Максимальный формат бумаги: PaperFormat.A0, PaperFormat.A1, PaperFormat.A2, PaperFormat.A3, PaperFormat.A4
#          Тип печати: PrintingType.Laser, PrintingType.Ink, PrintingType.BW, PrintingType.Color
#          Возможность подключения: Connectivity.USB, Connectivity.Wifi, Connectivity.Etherhet, Connectivity.AirPrint
#          Разрешение сканирования: ScanResolution.DPI600, ScanResolution.DPI1200, ScanResolution.DPI6400
#          Тип сканера: ScannerType.EdgeFed, ScannerType.FlatBed
# Введите параметры через пробел или пустую строку для выхода: ScannerType.FlatBed Connectivity.Wifi
# Результаты поиска:
#
# Информация об оборудовании: МФУ, модель Canon PIXMA G3411
#         Максимальный формат бумаги:
#                 A4
#         Тип печати:
#                 Струйная печать, Цветная печать
#         Разрешение сканирования:
#                 1200x1200 DPI
#         Возможность подключения:
#                 USB, Беспроводное подключение (Wifi)
#         Тип сканера:
#                 планшетный
# Количество на складе: 10
#
# Работа со складом, доступные операции:
#   [1] - Поиск оборудования по характеристикам на складе №1
#   [2] - Передача оборудования из склада №1 на склад №2
#   [3] - Показать содержимое складов
#   [4] - Выход
# Введите номер действия: 2
# Передача оборудования со склада №1 на склад №2
# Позиции доступные для передачи:
#         [0] Принтер Xerox Phaser 3020BI - 1 шт.
#         [1] Принтер HP DesignJet T230 (24-дюймовый) - 4 шт.
#         [2] Сканер Brother ADS-3600W - 9 шт.
#         [3] Сканер Mustek A3 1200S - 3 шт.
#         [4] МФУ Canon PIXMA G3411 - 10 шт.
#         [5] МФУ HP Laser MFP 135a - 9 шт.
# Введите номер позиции: 1
# Введите количество: 4
# Склад №1, выдано оборудование: Принтер HP DesignJet T230 (24-дюймовый) - 4 шт. Осталось на складе: 0 шт.
# Склад №2: принято оборудование Принтер HP DesignJet T230 (24-дюймовый), в количестве 4 шт.
# Работа со складом, доступные операции:
#   [1] - Поиск оборудования по характеристикам на складе №1
#   [2] - Передача оборудования из склада №1 на склад №2
#   [3] - Показать содержимое складов
#   [4] - Выход
# Введите номер действия: 3
# Содержимое складов:
#
# Склад №1, перечень оборудования:
#         Принтер Xerox Phaser 3020BI - 1 шт.
#         Сканер Brother ADS-3600W - 9 шт.
#         Сканер Mustek A3 1200S - 3 шт.
#         МФУ Canon PIXMA G3411 - 10 шт.
#         МФУ HP Laser MFP 135a - 9 шт.
#
# Склад №2, перечень оборудования:
#         Принтер HP DesignJet T230 (24-дюймовый) - 4 шт.
#
# Работа со складом, доступные операции:
#   [1] - Поиск оборудования по характеристикам на складе №1
#   [2] - Передача оборудования из склада №1 на склад №2
#   [3] - Показать содержимое складов
#   [4] - Выход
# Введите номер действия: 4