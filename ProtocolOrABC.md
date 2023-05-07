Both protocols and abstract classes serve similar purposes in Python, but there are some key differences between the two:

1. **Inheritance:** Abstract classes in Python can be inherited by other classes, while protocols cannot. Abstract classes are designed to be subclassed, and they can define some concrete methods or attributes in addition to the abstract methods that must be overridden by their subclasses. In contrast, protocols only define the methods and attributes that must be implemented by a class, without providing any implementation details.

2. **Composition over Inheritance:** Protocols encourage a compositional approach to programming, where a class can implement multiple protocols without being constrained by a single class hierarchy. This allows for greater flexibility and modularity in your code, as you can define protocols that describe specific behaviors or interfaces, and then mix and match them as needed. In contrast, abstract classes encourage an inheritance-based approach, where a class hierarchy is used to define a family of related classes that share some common behavior.

3. **Type Checking:** Protocols were introduced in Python 3.8 specifically to support type checking and static analysis tools. They provide a way to specify the expected interface of a class, which can be used to check if an object conforms to that interface at runtime. Abstract classes can also be used for type checking, but they are not as flexible as protocols, and they require more boilerplate code to define.

4. **Implementation:** Protocols are implemented using the `typing.Protocol` class, which is a special type of class that defines the interface of a protocol. Abstract classes are implemented using the `abc.ABC` class, which is a built-in abstract base class that allows you to define abstract methods and attributes.

In summary, while protocols and abstract classes share some similarities in their purpose, they have some key differences in terms of inheritance, composition, type checking, and implementation. Protocols are a newer feature in Python that were designed specifically for type checking and modularity, while abstract classes are a more traditional approach to defining abstract behavior in object-oriented programming.



The `PaymentProcessor` class in `processor.py` defines a concrete implementation of a payment processor. It has two methods, `validate_card` and `charge`, which validate a credit card and charge it with a given amount, respectively.

```py
class PaymentProcessor:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _check_api_key(self) -> bool:
        return self.api_key == API_KEY


    def validate_card(self, card: CreditCard, month: int, year: int) -> bool:
        if not 1 <= month <= 12:
            raise InvalidMonthError("Invalid expiry month. Month must be in the range of 1 to 12.")
        expiry_date = datetime(year, month, 1)
        if expiry_date < datetime.now():
            raise CardExpiredError("Card is expired.")
        if not luhn_checksum(card.number):
            raise ValueError("Invalid Card number")
        return True

    def charge(self, card: CreditCard, amount: int) -> None:
        try:
            self.validate_card(card, card.expiry_month, card.expiry_year)
        except CardExpiredError:
            raise CardExpiredError("Card validation failed: Card is expired.")
        except ValueError as e:
            raise ValueError(f"Card validation failed: {e}")
        if not self._check_api_key():
            raise ValueError("Invalid API key")
        print(f"Charging card number {card} for ${amount/100:.2f}")

```


The `PaymentProcessor` protocol in `payment.py` defines an interface or contract that any payment processor implementation must adhere to. It specifies that any class implementing this protocol must provide the `validate_card` and `charge` methods with specific signatures, but it doesn't provide any implementation details.



```py
class PaymentProcessor(Protocol):
    """A protocol defining the interface for payment processors.

    PaymentProcessor defines the required methods for any payment processor implementation.
    Any class implementing this protocol must provide the following methods:

    - validate_card(card: CreditCard, month: int, year: int) -> bool
    - charge(card: CreditCard, amount: int, month: int, year: int) -> bool
    """
    def validate_card(self, card: CreditCard, month: int, year: int) -> None:
        """Validates the card with the given expiry date"""
        pass

    def charge(self, card: str, amount: float) -> None:
        """Charges the card with the amount"""
        pass

```

By defining this protocol, you can write code that is not tied to a specific implementation of a payment processor. Instead, you can write code that relies on the `PaymentProcessor` protocol, and any class that implements this protocol can be used interchangeably. This allows for greater flexibility and modularity in your code, as you can easily swap out different payment processor implementations without having to change the code that uses them.

For example, you could have multiple payment processor implementations that conform to the `PaymentProcessor` protocol, such as one for PayPal - (`PayPalPaymnetProcessor(PaymentProcessor)`) and another for Stripe - (`StripePaymnetProcessor(PaymentProcessor)`) . You could then write code that uses the `PaymentProcessor` protocol, and you could instantiate the appropriate payment processor based on some configuration or user input.

The protocol also provides a way for type checkers and linters to verify that your code adheres to the expected interface. This can catch errors early on and make your code more reliable.