import uuid


class Human:
    inter = 44

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f'{self.name} is {self.age} years'

    @staticmethod
    def helo():
        return 'Hello'

    @classmethod
    def from_string(cls):
        return cls.inter


class Prefix_Name:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f'{self}'

    @staticmethod
    def concatenate_name(name: str) -> str:
        return f'{uuid.uuid4()}_{name}'
