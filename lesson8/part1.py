# 1. Реализовать класс «Дата», функция-конструктор которого должна принимать дату в виде строки формата «день-месяц-год». 
# В рамках класса реализовать два метода. Первый, с декоратором @classmethod, должен извлекать число, месяц, год и преобразовывать их тип к типу «Число». 
# Второй, с декоратором @staticmethod, должен проводить валидацию числа, месяца и года (например, месяц — от 1 до 12). 
# Проверить работу полученной структуры на реальных данных.

class Date():
    day: int
    month: int
    year: int

    def __init__(self, date_str):
        try:        
            self.day, self.month, self.year = map(int,date_str.split("-"))            
        except ValueError as ex:
            raise ValueError(f"Ошибка при разборе строки '{date_str}', требуемый формат ДД-ММ-ГГГГ") from ex

    @classmethod
    def parse(cls, date_str):
        """ разбор строки с датой в числа"""
        date = cls(date_str)
        return date.day, date.month, date.year

    @staticmethod
    def is_leap_year(year):
        """ 
        проверка является ли год високосным
        методика отсюда: https://docs.microsoft.com/ru-ru/office/troubleshoot/excel/determine-a-leap-year
        """
        if (year:=int(year)) < 0: raise ValueError("Год должен быть неотрицательным целым числом")        
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)                
        
    @staticmethod 
    def is_valid(date_str):
        """ проверка строки с датой на корректность """      
        day, month, year = Date.parse(date_str)
        # год не должен быть отрицательным
        if year < 0:
            return False
        # месяц в пределах от 1 до 12
        if month < 1 or month > 12:
            return False
        # день в пределах от 1 до максимального количества дней в заданном месяце заданного года
        days_count = [31, 29 if Date.is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]              
        if day < 1 or day > days_count[month-1]:
            return False
        
        return True


# проверка создания класса
print(f'Date("1-12-2021").year = {Date("1-12-2021").year}')

# проверка разбора даты на числа
print(f'Date.parse("1-12-2021") = {Date.parse("1-12-2021")}')

# проверка механизма поиска високосных годов
leap_years = [2000,2004,2008,2012,2016,2020,2024,2028,2032,2036,2040,2044]
passed = True
for year in range(2000,2045):
    if Date.is_leap_year(year):
        if year not in leap_years:
            print(f"Ошибка, год {year} високосный, а не то что тут насчитали!")
            passed = False
    else:
        if year in leap_years:
            print(f"Ошибка, год {year} не високосный, а не то что тут насчитали!")
            passed = False
print("Проверка расчета високосных годов", "пройдена!" if passed else "не пройдена :(")

# проверка валидации даты
passed = True

# с этими должно быть все ок
ok_dates = [
    "30-06-2001", 
    "29-02-2000", # високосный год, должно быть все ок
    "1     -      2       -     3", # так-то это тоже дата :)
]
for date in ok_dates:
    try:
        if not Date.is_valid(date):        
            print(f"Ошибка, дата '{date}' вполне нормальная, а не то что тут насчитали!")
            passed = False
    except ValueError as ex:
        print(f"Ошибка, которой быть не должно: {ex}")
        passed = False

# а тут все должно быть плохо!
fail_dates = [
    "31-06-2001",     # там только 30 дней
    "29-02-2001",     # не високосный год, так нельзя
    "кусь-кусь-кусь", # о, да
    "42-01-1900",     # cюда 42 нельзя
    "01-42-1900",     # да и сюда не стоит
]
for date in fail_dates:
    try:
        if Date.is_valid(date):        
            print(f"Ошибка, дата '{date}' - враки, а программа считает что все ок...")
            passed = False
    except ValueError:        
        # это как раз нормально
        pass
    
print("Проверка валидации дат", "пройдена!" if passed else "не пройдена :(")

# результат запуска программы:
# Date("1-12-2021").year = 2021
# Date.parse("1-12-2021") = (1, 12, 2021)
# Проверка расчета високосных годов пройдена!
# Проверка валидации дат пройдена!