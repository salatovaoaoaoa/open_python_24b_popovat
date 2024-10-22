class Base:
    _name = None

    def __set_name__(self, _, name):
        self._name = f"_hidden_{name}"

    def __get__(self, obj, _):
        if obj is None:
            return None

        return getattr(obj, self._name)

    def __set__(self, obj, val):
        if obj is None:
            return None

        self.validate(val)

        setattr(obj, self._name, val)

    def __delete__(self, obj):
        if obj is None:
            return None

        delattr(obj, self._name)

    def validate(self, _):
        raise NotImplementedError("Implement me!")


class String(Base):
    """Дескриптор для учета имени гостя"""

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"{type(value).__name__} is not str")
        if not value.strip():
            raise ValueError("String cannot be empty")


class Integer(Base):
    """Дескриптор для положительных целых чисел (для учета гостей)"""

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"{type(value).__name__} is not int")


class PositiveFloat(Base):
    """Дескриптор для положительных вещественных чисел (для учета деняк)"""

    def validate(self, value):
        if not isinstance(value, float):
            raise ValueError(f"{type(value).__name__} is not a float")
        if value <= 0:
            raise ValueError(f"{value} is below zero")


class WeddingData:
    counter = Integer()
    money = PositiveFloat()
    name = String()

    def __init__(self, counter, money, name):
        self.counter = counter
        self.money = money
        self.name = name
