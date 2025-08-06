"""
Реализуйте паттерн синглтон тремя способами:

с помощью метаклассов
с помощью метода __new__ класса
через механизм импортов
"""


# Через метакласс
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value


a = Singleton(10)
b = Singleton(20)
print(a is b)
print(a.value, b.value)


# Через переопределение __new__
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value


a = Singleton(10)
b = Singleton(20)
print(a is b)
print(a.value, b.value)


# Через механизм импортов
class _Singleton:
    def __init__(self, value):
        self.value = value


instance = _Singleton(10)

a = instance
b = instance
print(a is b)
print(a.value, b.value)
