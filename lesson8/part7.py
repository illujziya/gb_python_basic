# 7. Реализовать проект «Операции с комплексными числами». 
# Создайте класс «Комплексное число», реализуйте перегрузку методов сложения и умножения комплексных чисел. 
# Проверьте работу проекта, создав экземпляры класса (комплексные числа) и выполнив сложение и умножение созданных экземпляров. 
# Проверьте корректность полученного результата.

class ComplexNumber():
    """
        Класс для работы с комплексными числами
        Поддерживается сложение, умножение и проверка на равенство
        Формулы согласно https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%BD%D0%BE%D0%B5_%D1%87%D0%B8%D1%81%D0%BB%D0%BE
    """
    def __init__(self,a,b):
        """ комплексное число (int,int)"""
        try:
            self.a = int(a)
            self.b = int(b)
        except ValueError as ex:
            raise(f"ошибка при создании числа - аргументы должны быть вещественными числами!", ex)

    def __str__(self):
        return f"{self.a}{'+' if self.b>=0 else ''}{self.b}i"

    def __add__(self, other):
        """ сложение """
        if type(other) != ComplexNumber: 
            raise TypeError("комплексные числа можно складывать только с другими комплексными числами") 
        return ComplexNumber(self.a+other.a, self.b + other.b)

    def __mul__(self, other):
        """ умножение """
        if type(other) != ComplexNumber: 
            raise TypeError("комплексные числа можно умножать только на другие комплексные числа") 
        a = self.a * other.a - self.b * other.b
        b = self.b * other.a + self.a * other.b
        return ComplexNumber(a, b)

    def __eq__(self,other) -> bool:
        """ проверка на равенство """
        return (self.a == other.a) and (self.b == other.b)

# проверка создания числа
x = ComplexNumber(1,-2)
y = ComplexNumber(3,4)
print(f"ComplexNumber(1,-2) = {ComplexNumber(1,-2)}")
print(f"ComplexNumber(3,4) = {ComplexNumber(3,4)}")

# проверка равенства
print(f"{x} == {x} это: {x == x}")
print(f"{x} == {y} это: {x == y}")

# проверка сложения чисел
x_add_y = ComplexNumber(4,2)   # заведомо правильный ответ для проверки
print(f"({x}) + ({y}) = {x+y} (должно получиться {x_add_y}: {x+y==x_add_y})")

# проверка умножения чисел
x_mul_y = ComplexNumber(11,-2) # ответ для проверки
print(f"({x}) * ({y}) = {x*y} (должно получиться {x_mul_y}: {x*y==x_mul_y})")

# Результат запуска программы:
# ComplexNumber(1,-2) = 1-2i
# ComplexNumber(3,4) = 3+4i
# 1-2i == 1-2i это: True
# 1-2i == 3+4i это: False
# (1-2i) + (3+4i) = 4+2i (должно получиться 4+2i: True)
# (1-2i) * (3+4i) = 11-2i (должно получиться 11-2i: True)