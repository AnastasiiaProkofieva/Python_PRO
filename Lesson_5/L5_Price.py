from typing import Any


class Price:
    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def __add__(self, other) -> 'Price':
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only with Prices objects')
        else:
            if self.currency != other.currency:
                """
                1USD = 0.88CHR;
                1EUR = 0.93CHR
                1CHR = 1.13USD = 1.08EUR
                """
                if self.currency == 'USD' and other.currency == 'EUR':
                    return Price(value=round((self.value*0.88 + other.value*0.93)*1.13, 2), currency=self.currency)
                elif self.currency == 'EUR' and other.currency == 'USD':
                    return Price(value=round((self.value*0.93 + other.value*0.88)*1.08, 2), currency=self.currency)
                else:
                    raise ValueError("The option is unavailable: lack of currencies' types")

            return Price(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other) -> 'Price':
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only with Prices objects')
        else:
            if self.currency != other.currency:
                raise ValueError("The option is unavailable: different type of currencies")
            elif self.value < other.value:
                return Price(value=other.value - self.value, currency=self.currency)
            else:
                return Price(value=self.value - other.value, currency=self.currency)


Price_A = Price(value=100, currency='USD')
Price_B = Price(value=200, currency='USD')
Price_C = Price(value=100, currency='EUR')

total: Price = Price_A + Price_B
total_dif: Price = Price_B + Price_C
sub: Price = Price_A - Price_B
print(total)
print(total_dif)
print(sub)
