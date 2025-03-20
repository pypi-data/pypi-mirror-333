"""

 Author: Oscar Maldonado
 Email: oscarmmgg1234@gmail.com

 Creation Date: 2025-03-12 16:42:59

 temp

"""
from decimal import Decimal
import re

class SNotation:
    """Handles scientific notation parsing, arithmetic, and custom output formatting."""

    def __init__(self, value):
        self.value = self.parse_input(value)

    def parse_input(self, value):
        """Parses input into a Decimal number while supporting flexible scientific notation."""
        if isinstance(value, SNotation):
            return value.value  # Extract the Decimal value from another SNotation object

        if isinstance(value, (int, float, Decimal)):
            return Decimal(value)

        if isinstance(value, str):
            # Handle formats like "8.99 x 10^9", "8.99e9", "8.99E9"
            formatted_value = value.replace(" x 10^", "E").replace("^", "")
            sci_notation_match = re.fullmatch(r"([-+]?\d*\.?\d+)[Ee]?([-+]?\d+)?", formatted_value)

            if sci_notation_match:
                base, exponent = sci_notation_match.groups()
                exponent = exponent if exponent is not None else "0"
                return Decimal(f"{base}E{exponent}")

            raise ValueError(f"Invalid scientific notation format: {value}")

        raise TypeError(f"Unsupported type for SNotation: {type(value)}")

    def to_standard_notation(self):
        """Returns the value as a standard float."""
        return float(self.value)

    def to_scientific_notation(self, format_type="E"):
        """
        Returns the number formatted in different scientific notation styles.

        :param format_type: Choose `"E"` (default) for "3.20E+04",
                            `"x"` for "3.20 x 10^4",
                            `"e"` for "3.20e+04".
        """
        base, exponent = f"{self.value:.5E}".split("E")
        exponent = int(exponent)  # Convert exponent to integer

        if format_type.upper() == "E":
            return f"{base}E{exponent}"
        elif format_type == "x":
            return f"{base} x 10^{exponent}"
        elif format_type == "e":
            return f"{base}e{exponent}"
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def __str__(self):
        """Default string representation: float value."""
        return str(self.to_standard_notation())

    # ✅ Ensuring all operations return an SNotation object
    def __add__(self, other):
        return SNotation(self.value + self.parse_input(other))

    def __sub__(self, other):
        return SNotation(self.value - self.parse_input(other))

    def __mul__(self, other):
        return SNotation(self.value * self.parse_input(other))

    def __truediv__(self, other):
        return SNotation(self.value / self.parse_input(other))

    def __pow__(self, exponent):
        return SNotation(self.value ** self.parse_input(exponent))
    