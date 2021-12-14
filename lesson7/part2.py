# 2. Реализовать проект расчета суммарного расхода ткани на производство одежды. 
# Основная сущность (класс) этого проекта — одежда, которая может иметь определенное название. 
# К типам одежды в этом проекте относятся пальто и костюм. У этих типов одежды существуют параметры: размер (для пальто) и рост (для костюма). 
# Это могут быть обычные числа: V и H, соответственно.
# Для определения расхода ткани по каждому типу одежды использовать формулы: для пальто (V/6.5 + 0.5), для костюма (2*H + 0.3). 
# Проверить работу этих методов на реальных данных.
# Реализовать общий подсчет расхода ткани. 
# Проверить на практике полученные на этом уроке знания: реализовать абстрактные классы для основных классов проекта, проверить на практике работу декоратора @property.

from abc import ABC, abstractmethod

class Clothes(ABC):
    def __init__(self, param):
        self.param = param

    @abstractmethod
    def consumption(self):
        pass

class Coat(Clothes):
    @property
    def consumption(self):
        return self.param/6.5 + 0.5

    @property 
    def size(self):
        return self.param

class Costume(Clothes):
    @property
    def consumption(self):
        return 2*self.param + 0.3

    @property 
    def tall(self):
        return self.param

big_coat = Coat(82)
nice_costume = Costume(55)

print(f"Расход ткани для пальто ({big_coat.size} размер) - {big_coat.consumption:.2f}, для костюма (рост {nice_costume.tall})- {nice_costume.consumption:.2f}")
print(f"Всего ткани нужно - {big_coat.consumption + nice_costume.consumption:.2f}")

# Результат запуска:
# Расход ткани для пальто (82 размер) - 13.12, для костюма (рост 55)- 110.30
# Всего ткани нужно - 123.42