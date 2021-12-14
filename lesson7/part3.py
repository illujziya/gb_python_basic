# 3. Реализовать программу работы с органическими клетками, состоящими из ячеек.
# Необходимо создать класс Клетка. В его конструкторе инициализировать параметр, соответствующий количеству ячеек клетки (целое число). 
# В классе должны быть реализованы методы перегрузки арифметических операторов: сложение (add()), вычитание (sub()), умножение (mul()), деление (truediv()). 
# Данные методы должны применяться только к клеткам и выполнять увеличение, уменьшение, умножение и целочисленное (с округлением до целого) деление клеток, соответственно.
# Сложение. Объединение двух клеток. При этом число ячеек общей клетки должно равняться сумме ячеек исходных двух клеток.
# Вычитание. Участвуют две клетки. Операцию необходимо выполнять только если разность количества ячеек двух клеток больше нуля, иначе выводить соответствующее сообщение.
# Умножение. Создается общая клетка из двух. Число ячеек общей клетки определяется как произведение количества ячеек этих двух клеток.
# Деление. Создается общая клетка из двух. Число ячеек общей клетки определяется как целочисленное деление количества ячеек этих двух клеток.
# В классе необходимо реализовать метод make_order(), принимающий экземпляр класса и количество ячеек в ряду. Данный метод позволяет организовать ячейки по рядам.
# Метод должен возвращать строку вида *****\n*****\n*****..., где количество ячеек между \n равно переданному аргументу. 
# Если ячеек на формирование ряда не хватает, то в последний ряд записываются все оставшиеся.
# Например, количество ячеек клетки равняется 12, количество ячеек в ряду — 5. Тогда метод make_order() вернет строку: *****\n*****\n**.
# Или, количество ячеек клетки равняется 15, количество ячеек в ряду — 5. Тогда метод make_order() вернет строку: *****\n*****\n*****.

class Cell():    
    def __init__(self, value):
        if type(value) != int or value < 1:
            raise ValueError("Количество ячеек новой клетки должно быть целым положительным числом больше 0")
        self.size = value

    def __str__(self):
        return f"Клетка({self.size})"

    def __add__(self, other):
        if type(other) != Cell:
            raise ValueError("Клетки складываются только с клетками!")
        return Cell(self.size + other.size)
    
    def __sub__(self, other):
        if type(other) != Cell:
            raise ValueError("Из клетки можно вычесть только другую клетку!")
        return Cell(self.size - other.size)

    def __mul__(self, other):
        if type(other) != Cell:
            raise ValueError("Клетку можно умножить только на другую клетку!")
        return Cell(self.size * other.size)    
    
    def __truediv__(self, other):
        if type(other) != Cell:
            raise ValueError("Клетку можно делить только на другую клетку!")
        return Cell(self.size // other.size) 

    def make_order(self, row):
        # полные ряды, если есть
        lines = ["*" * row] * (self.size // row)

        # остаточек, если есть
        symbols_left = self.size % row
        if symbols_left>0:
            lines.append("*" * symbols_left)
                
        return "\n".join(lines)

# базовые операции
a = Cell(3)
b = Cell(2)
print(f"{a} + {b} = {a+b}")
print(f"{a} - {b} = {a-b}")
print(f"{a} * {b} = {a*b}")
print(f"{a} / {b} = {a/b}")

# метод make_order()
print("Метод make_order():")
for num in [15,13,4]:
    print(f"Cell({num}).make_order(5) = \n{Cell(num).make_order(5)}")

print("Обработка ошибок:")
# кривые клетки
for num in [0,"джигурда",-9000]:
    try:
        wrong_cell = Cell(-2)
    except Exception as ex:
        print(f"Cell({num}) = Ошибка: {ex}")
# вычитание
try:
    print(f"{b} - {a} = {b-a}")
except Exception as ex:
    print(f"{b} - {a} = Ошибка: {ex}")
# клетка и не клетка
try:
    print(f'{a} - "котик" = {a - "котик"}')
except Exception as ex:
    print(f'{a} - "котик" = Ошибка: {ex}')

# Результат запуска:
# Клетка(3) + Клетка(2) = Клетка(5)
# Клетка(3) - Клетка(2) = Клетка(1)
# Клетка(3) * Клетка(2) = Клетка(6)
# Клетка(3) / Клетка(2) = Клетка(1)
# Метод make_order():
# Cell(15).make_order(5) = 
# *****
# *****
# *****
# Cell(13).make_order(5) = 
# *****
# *****
# ***
# Cell(4).make_order(5) = 
# ****
# Обработка ошибок:
# Cell(0) = Ошибка: Количество ячеек новой клетки должно быть целым положительным числом больше 0
# Cell(джигурда) = Ошибка: Количество ячеек новой клетки должно быть целым положительным числом больше 0
# Cell(-9000) = Ошибка: Количество ячеек новой клетки должно быть целым положительным числом больше 0
# Клетка(2) - Клетка(3) = Ошибка: Количество ячеек новой клетки должно быть целым положительным числом больше 0
# Клетка(3) - "котик" = Ошибка: Из клетки можно вычесть только другую клетку!