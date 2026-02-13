def caching_fibonacci():
    """
    Creates a function for computing Fibonacci numbers with caching.

    Uses closure to store the cache of computed values.
    This allows avoiding repeated computations of the same values.

    Returns:
        function: The inner fibonacci(n) function for computing the n-th Fibonacci number
    """
    # Cache for storing already computed Fibonacci numbers
    # This dictionary is accessible to the inner function thanks to closure
    cache = {}

    def fibonacci(n):
        """
        Computes the n-th Fibonacci number using cache.

        First checks if the value is already in the cache.
        If yes, returns the value from the cache.
        If no, computes recursively, stores in cache and returns the result.

        Args:
            n (int): The ordinal number of the Fibonacci number

        Returns:
            int: The n-th number of the Fibonacci sequence
        """
        # Base cases: F(0) = 0, F(1) = 1
        if n <= 1:
            return n

        # Check if the value is already computed and stored in cache
        if n in cache:
            return cache[n]

        # If the value is not in cache, compute it recursively
        # F(n) = F(n-1) + F(n-2)
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        # Return the computed value
        return cache[n]

    # Return the inner function that will have access to cache through closure
    return fibonacci


# Example usage
if __name__ == "__main__":
    # Create a function for computing Fibonacci
    fib = caching_fibonacci()

    # Compute the first 10 Fibonacci numbers
    print("First 10 Fibonacci sequence numbers:")
    for i in range(10):
        print(f"F({i}) = {fib(i)}")

    # Demonstrating the effectiveness of caching
    print("\nLarger numbers (caching significantly speeds up computation):")
    print(f"F(10) = {fib(10)}")
    print(f"F(12) = {fib(12)}")
    print(f"F(35) = {fib(35)}")
    print(f"F(40) = {fib(40)}")
