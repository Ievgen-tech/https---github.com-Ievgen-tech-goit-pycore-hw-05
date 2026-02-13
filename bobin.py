import re
from typing import Callable


def generator_numbers(text: str):
    """
    Generator function that identifies and yields all valid numbers from text.

    This function uses regular expressions to find all numbers in the text
    that are clearly separated by spaces on both sides. Each valid number
    is yielded one at a time, making this a memory-efficient generator.

    Args:
        text (str): The input text containing numbers to be extracted

    Yields:
        float: Each valid number found in the text as a float

    Example:
        >>> text = "Profit: 100 points, Loss: 50 points, Income: 200 points"
        >>> for number in generator_numbers(text):
        ...     print(number)
        100.0
        50.0
        200.0
    """
    # Regular expression pattern to match numbers
    # The pattern \b\d+\.?\d*\b matches:
    # \b - word boundary (ensures number is clearly separated by spaces)
    # \d+ - one or more digits
    # \.? - optional decimal point
    # \d* - zero or more digits after decimal point
    pattern = r'\b\d+\.?\d*\b'

    # Find all matches of the pattern in the text
    for match in re.finditer(pattern, text):
        # Convert matched string to float and yield it
        yield float(match.group())


def sum_profit(text: str, func: Callable) -> float:
    """
    Calculates the total sum of all valid numbers in the text.

    This function uses a generator function to efficiently process
    numbers from the text and returns their sum. It accepts a callable
    (generator function) as an argument.

    Args:
        text (str): The input text containing numbers to sum
        func (Callable): A generator function that yields numbers from text
                        (typically generator_numbers)

    Returns:
        float: The sum of all valid numbers found in the text

    Example:
        >>> text = "Profit: 100 points, Loss: 50 points, Income: 200 points"
        >>> total = sum_profit(text, generator_numbers)
        >>> print(total)
        350.0
    """
    # Use the generator function to get all numbers from the text
    # and sum them using the built-in sum() function
    return sum(func(text))


# Example usage and testing
if __name__ == "__main__":
    # Example text with multiple numbers
    sample_text = "Profit from January: 150.50 UAH, February: 200 UAH, March: 175.75 UAH"

    # Display the original text
    print("Text:", sample_text)
    print()

    # Extract and display individual numbers using the generator
    print("Numbers extracted by generator:")
    for number in generator_numbers(sample_text):
        print(f"  - {number}")

    print()

    # Calculate and display the total sum
    total_profit = sum_profit(sample_text, generator_numbers)
    print(f"Total sum of all numbers: {total_profit}")

    print("\n" + "="*50 + "\n")

    # Additional test case
    sample_text2 = "Sales: 1000 2500.99 3200.50 Marketing costs: 500 1200.75"
    print("Text:", sample_text2)
    print()

    print("Numbers extracted by generator:")
    for number in generator_numbers(sample_text2):
        print(f"  - {number}")

    print()

    total_profit2 = sum_profit(sample_text2, generator_numbers)
    print(f"Total sum of all numbers: {total_profit2}")
