# date: 2021/3/25
from decimal import Decimal

from numpy import random as np

print(np.random(5))
print(np.random() - 0.5)

list1 = np.random(5)
list2 = []
print(list1)
for index, value in enumerate(list1):
    list2.append(value / 2)

print(list2)

a = Decimal(str(1.1))
b = Decimal(str(2))
print(f'decimal: {a / b}')