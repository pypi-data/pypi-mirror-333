"""Module for the KnownProblems class"""

# Standard Modules
import math


class KnownProblems:
    """
    This class has the implementation of some of the usual problems that you always forget and need
    to go watch the solution on StackOverflow even though you know you've already solved them.
    """

    _ERRORS: dict[str, str] = {
        "constructor": "This class is not instantiable!",
        "values": "Too few arguments were passed!",
    }

    def __init__(self) -> None:
        """Prevents the instantiation of this class.

        Raises
        ------
        - NotImplementedError
        """
        raise NotImplementedError(KnownProblems._ERRORS["constructor"])

    @staticmethod
    def _mcd(a: int, b: int) -> int:
        """Finds the MCD (Maximum Common Divider) between two integers.

        Params
        ------
        - `a` -> The first number to calculate the MCD.
        - `b` -> The second number to calculate the MCD.

        Returns
        -------
        An integer representing the MCD.
        """
        while a != 0 and b != 0:
            if a > b:
                a %= b
            else:
                b %= a

        return b if a == 0 else a

    @staticmethod
    def mcd(values: list[int]) -> int:
        """Finds the MCD (Maximum Common Divider) between a list of integers.

        Params
        ------
        - `values` -> The values used to find the MCD.

        Returns
        -------
        An integer representing the MCD between all the values.

        Raises
        ------
        - `ValueError` -> If less than two values are given.
        """
        if not values or len(values) < 2:
            raise ValueError(KnownProblems._ERRORS["values"])

        mcd: int = values[0]

        for value in values[1:]:
            mcd = KnownProblems._mcd(mcd, value)

        return mcd

    @staticmethod
    def _mcm(a: int, b: int) -> int:
        """Finds the MCM (Minimum Common Multiplier) between two numbers.

        Params
        ------
        - `a` -> The first number to calculate the MCM.
        - `b` -> The second number to calculate the MCM.

        Returns
        -------
        An integer representing the MCM.
        """
        mcd: int = KnownProblems._mcd(a, b)

        return (a * b) // mcd

    @staticmethod
    def mcm(values: list[int]) -> int:
        """Finds the MCM (Minimum Common Multiplier) between a list of integers.

        Params
        ------
        - `values` -> The values used to find the MCM.

        Returns
        -------
        An integer representing the MCM between all the values.

        Raises
        ------
        - `ValueError` -> If less than two values are given.
        """
        if not values or len(values) < 2:
            raise ValueError(KnownProblems._ERRORS["values"])

        mcm: int = values[0]

        for value in values[1:]:
            mcm = KnownProblems._mcm(mcm, value)

        return mcm

    @staticmethod
    def count_integer_digits(n: int) -> int:
        """Counts the number of digits of an integer.

        Params
        ------
        - `n` -> The number to calculate the digits.

        Returns
        -------
        An integer representing the number of digits of `n`.
        """
        return len(str(abs(n)))

    @staticmethod
    def count_decimal_digits(n: float) -> int:
        """Counts the number of decimal digits in a float.

        Params
        ------
        - `n` -> The number to calculate the decimal digits.

        Returns
        -------
        An integer representing the number of decimal digits of `n`.
        """
        splitted_number: list[str] = str(abs(n)).split(".")

        if len(splitted_number) < 2:
            return 0

        return len(splitted_number[1])

    @staticmethod
    def sieve_of_eratosthenes(n: int) -> list[int]:
        """Finds the prime numbers from 2 to `n` using the Sieve of Eratosthenes algorithm. This
        algorithm greatly decreases in speed the more we increase `n`, but it's still the simplest
        way of finding prime numbers.

        Params
        ------
        - `n` -> The limit of the sieve where to search for prime numbers.

        Returns
        -------
        A list of integers representing the prime numbers frm 2 to `n`.
        """
        primes: list[int] = []
        sieve: set[int] = set(range(2, n + 1))

        while sieve:
            prime = min(sieve)
            primes.append(prime)
            sieve -= set(range(prime, n + 1, prime))

        return primes

    @staticmethod
    def sieve_of_atkin(limit: int) -> list[int]:
        """Finds the prime numbers from 2 to limit. Builds on the concept of the sieve of
        Eratosthenes but it's way faster even though the algorithm is more complex.

        Params
        ------
        - `limit` -> The limit of the sieve where to search for prime numbers.

        Returns
        -------
        A list of integers representing the prime numbers frm 2 to `limit`.
        """
        primes: list[int] = [2, 3, 5]
        sieve: list[bool] = [False] * (limit + 1)
        constraint = int(math.sqrt(limit)) + 1

        for x in range(1, constraint):
            for y in range(1, constraint):
                n = 4 * x**2 + y**2
                r = n % 12
                if n <= limit and r in (1, 5):
                    sieve[n] = not sieve[n]

                n = 3 * x**2 + y**2
                r = n % 12
                if n <= limit and r == 7:
                    sieve[n] = not sieve[n]

                n = 3 * x**2 - y**2
                r = n % 12
                if x > y and n <= limit and r == 11:
                    sieve[n] = not sieve[n]

        constraint -= 1
        for x in range(5, constraint):
            if sieve[x]:
                for y in range(x**2, limit + 1, x**2):
                    sieve[y] = False

        for i in range(7, limit + 1):
            if sieve[i]:
                primes.append(i)

        return primes
