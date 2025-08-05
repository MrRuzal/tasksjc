'''
Напишите метакласс, который автоматически добавляет атрибут created_at
с текущей датой и временем к любому классу, который его использует.
'''

from datetime import datetime


class AutoCreatedAtMeta(type):
    """Метакласс, добавляющий created_at с временем создания класса."""

    def __new__(cls, name, bases, namespace):
        namespace['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, namespace)


class MyClass(metaclass=AutoCreatedAtMeta):
    pass


print(MyClass.created_at)
