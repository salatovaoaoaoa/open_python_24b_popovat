import random


class SomeModel:

    def predict(self, message: str) -> float:

        num = len(message)
        random_value = random.uniform(0, num**2 / 50) if num > 0 else 0

        return random_value

    def fun_message(self) -> str:
        return "have a nice day"
