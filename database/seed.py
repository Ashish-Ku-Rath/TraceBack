"""
Initial problem seed data for TraceBack.
Provides an idempotent seed mechanism that populates the database with initial DSA problems.
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from backend.models.problem import Problem, ProblemExample
from database.connection import SessionLocal, init_db

# Initial problem definitions with complete-program mode specifications and sample test cases
INITIAL_PROBLEMS: List[Dict[str, Any]] = [
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Map"],
        "description": (
            "Given an integer array `nums` and an integer `target`, determine and return "
            "the 0-based indices of the two elements whose sum equals `target`.\n\n"
            "### Input Format\n"
            "- Line 1: An integer `n`, the number of elements in the array.\n"
            "- Line 2: `n` space-separated integers representing the array `nums`.\n"
            "- Line 3: An integer `target`.\n\n"
            "### Output Format\n"
            "- Print the two 0-based indices separated by a space (e.g. `0 1`).\n\n"
            "### Assumptions\n"
            "- Exactly one valid solution exists for each test case.\n"
            "- You cannot use the same array element twice.\n"
            "- The answer indices can be printed in any order."
        ),
        "constraints": (
            "2 <= nums.length <= 10^4\n"
            "-10^9 <= nums[i] <= 10^9\n"
            "-10^9 <= target <= 10^9\n"
            "Exactly one valid solution exists."
        ),
        "examples": [
            {
                "input": "4\n2 7 11 15\n9",
                "expected_output": "0 1",
                "explanation": "Because nums[0] + nums[1] == 2 + 7 == 9, return indices 0 and 1.",
            },
            {
                "input": "3\n3 2 4\n6",
                "expected_output": "1 2",
                "explanation": "Because nums[1] + nums[2] == 2 + 4 == 6, return indices 1 and 2.",
            },
            {
                "input": "2\n3 3\n6",
                "expected_output": "0 1",
                "explanation": "Because nums[0] + nums[1] == 3 + 3 == 6, return indices 0 and 1.",
            },
        ],
    },
    {
        "title": "Reverse String",
        "slug": "reverse-string",
        "difficulty": "Easy",
        "tags": ["String", "Two Pointers"],
        "description": (
            "Write a program that takes an input string and outputs the reversed string.\n\n"
            "### Input Format\n"
            "- Line 1: A single line string `s`.\n\n"
            "### Output Format\n"
            "- Print the reversed string on a single line."
        ),
        "constraints": (
            "1 <= s.length <= 10^5\n"
            "s consists of printable ASCII characters."
        ),
        "examples": [
            {
                "input": "hello",
                "expected_output": "olleh",
                "explanation": "The string characters are reversed.",
            },
            {
                "input": "Hannah",
                "expected_output": "hannaH",
                "explanation": "Case is preserved and all characters are reversed.",
            },
        ],
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "Medium",
        "tags": ["String", "Stack"],
        "description": (
            "Given a string `s` containing only the characters '(', ')', '{', '}', '[' and ']', "
            "determine whether the bracket sequence is structurally valid.\n\n"
            "### Input Format\n"
            "- Line 1: A single string `s` containing brackets.\n\n"
            "### Output Format\n"
            "- Print `true` if the string is valid, or `false` otherwise.\n\n"
            "A bracket sequence is valid if and only if:\n"
            "1. Every open bracket is closed by a matching bracket of the identical type.\n"
            "2. Open brackets are closed in the exact order of their nesting.\n"
            "3. Every closing bracket matches a previously opened bracket."
        ),
        "constraints": (
            "1 <= s.length <= 10^4\n"
            "s consists exclusively of parentheses: '()[]{}'."
        ),
        "examples": [
            {
                "input": "()[]{}",
                "expected_output": "true",
                "explanation": "All three bracket pairs open and close in correct sequence.",
            },
            {
                "input": "(]",
                "expected_output": "false",
                "explanation": "The open parenthesis '(' is incorrectly closed by square bracket ']'.",
            },
            {
                "input": "([)]",
                "expected_output": "false",
                "explanation": "The parentheses and brackets interleave out of order.",
            },
        ],
    },
    # -------------------------------------------------------------------------
    # 20 NEW PROBLEMS (Problems 4 - 23)
    # -------------------------------------------------------------------------
    {
        "title": "Fibonacci Series",
        "slug": "fibonacci-series",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Given an integer `N`, print the first `N` numbers of the Fibonacci sequence.\n"
            "The sequence starts with 0 and 1, where each subsequent number is the sum of the previous two "
            "(0, 1, 1, 2, 3, 5, 8, ...).\n\n"
            "### Input Format\n"
            "- Line 1: A single integer `N`.\n\n"
            "### Output Format\n"
            "- Print the first `N` Fibonacci numbers separated by spaces on a single line."
        ),
        "constraints": "1 <= N <= 40",
        "examples": [
            {"input": "5", "expected_output": "0 1 1 2 3", "explanation": "The first 5 Fibonacci numbers."},
            {"input": "1", "expected_output": "0", "explanation": "The first 1 Fibonacci number is 0."},
            {"input": "2", "expected_output": "0 1", "explanation": "The first 2 Fibonacci numbers are 0 and 1."},
            {"input": "8", "expected_output": "0 1 1 2 3 5 8 13", "explanation": "The first 8 Fibonacci numbers."},
            {"input": "10", "expected_output": "0 1 1 2 3 5 8 13 21 34", "explanation": "The first 10 Fibonacci numbers."},
        ],
    },
    {
        "title": "Armstrong Number",
        "slug": "armstrong-number",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Determine whether a given non-negative integer `N` is an Armstrong number.\n"
            "An Armstrong number of `k` digits is an integer such that the sum of its digits "
            "each raised to the power of `k` equals the number itself.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if `N` is an Armstrong number, or `No` otherwise."
        ),
        "constraints": "0 <= N <= 10^7",
        "examples": [
            {"input": "153", "expected_output": "Yes", "explanation": "1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153."},
            {"input": "370", "expected_output": "Yes", "explanation": "3^3 + 7^3 + 0^3 = 27 + 343 + 0 = 370."},
            {"input": "120", "expected_output": "No", "explanation": "1^3 + 2^3 + 0^3 = 1 + 8 + 0 = 9 != 120."},
            {"input": "9", "expected_output": "Yes", "explanation": "9^1 = 9."},
            {"input": "9474", "expected_output": "Yes", "explanation": "9^4 + 4^4 + 7^4 + 4^4 = 6561 + 256 + 2401 + 256 = 9474."},
        ],
    },
    {
        "title": "Palindrome Number",
        "slug": "palindrome-number",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Determine whether a given non-negative integer reads the same forward and backward.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if the number is a palindrome, or `No` otherwise."
        ),
        "constraints": "0 <= N <= 10^9",
        "examples": [
            {"input": "121", "expected_output": "Yes", "explanation": "121 reads the same backward as forward."},
            {"input": "123", "expected_output": "No", "explanation": "123 reversed is 321."},
            {"input": "0", "expected_output": "Yes", "explanation": "0 is a single digit palindrome."},
            {"input": "1221", "expected_output": "Yes", "explanation": "1221 reads the same backward as forward."},
            {"input": "1000", "expected_output": "No", "explanation": "1000 reversed is 1."},
        ],
    },
    {
        "title": "Prime Number",
        "slug": "prime-number",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Check whether a given integer `N` is prime.\n"
            "A prime number is an integer strictly greater than 1 that has no positive divisors other than 1 and itself.\n"
            "Negative numbers, 0 and 1 are NOT prime.\n\n"
            "### Input Format\n"
            "- Line 1: An integer `N`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if `N` is prime, or `No` otherwise."
        ),
        "constraints": "-10^6 <= N <= 10^7",
        "examples": [
            {"input": "7", "expected_output": "Yes", "explanation": "7 has only divisors 1 and 7."},
            {"input": "1", "expected_output": "No", "explanation": "1 is by definition not a prime number."},
            {"input": "0", "expected_output": "No", "explanation": "0 is not a prime number."},
            {"input": "-5", "expected_output": "No", "explanation": "Negative numbers are not prime."},
            {"input": "29", "expected_output": "Yes", "explanation": "29 has no divisors other than 1 and 29."},
        ],
    },
    {
        "title": "Factorial",
        "slug": "factorial",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Calculate the factorial of a given non-negative integer `N`.\n"
            "The factorial of `N` (denoted `N!`) is the product of all positive integers less than or equal to `N`.\n"
            "By definition, 0! = 1.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print the factorial value of `N`."
        ),
        "constraints": "0 <= N <= 20",
        "examples": [
            {"input": "5", "expected_output": "120", "explanation": "5! = 5 * 4 * 3 * 2 * 1 = 120."},
            {"input": "0", "expected_output": "1", "explanation": "0! = 1 by definition."},
            {"input": "1", "expected_output": "1", "explanation": "1! = 1."},
            {"input": "7", "expected_output": "5040", "explanation": "7! = 5040."},
            {"input": "10", "expected_output": "3628800", "explanation": "10! = 3628800."},
        ],
    },
    {
        "title": "Reverse a Number",
        "slug": "reverse-a-number",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Given a non-negative integer `N`, reverse its digits and print the resulting integer without leading zeros.\n"
            "If `N` is 0, output `0`.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print the reversed integer."
        ),
        "constraints": "0 <= N <= 10^9",
        "examples": [
            {"input": "12345", "expected_output": "54321", "explanation": "Digits reversed."},
            {"input": "100", "expected_output": "1", "explanation": "Trailing zeros become leading and are omitted."},
            {"input": "0", "expected_output": "0", "explanation": "Reversing 0 gives 0."},
            {"input": "7", "expected_output": "7", "explanation": "Single digit reversed is itself."},
            {"input": "9080", "expected_output": "809", "explanation": "9080 reversed without leading zeros is 809."},
        ],
    },
    {
        "title": "Sum of Digits",
        "slug": "sum-of-digits",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Calculate and print the sum of all digits of a given non-negative integer `N`.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print the sum of the digits of `N`."
        ),
        "constraints": "0 <= N <= 10^12",
        "examples": [
            {"input": "1234", "expected_output": "10", "explanation": "1 + 2 + 3 + 4 = 10."},
            {"input": "0", "expected_output": "0", "explanation": "The sum of digits of 0 is 0."},
            {"input": "999", "expected_output": "27", "explanation": "9 + 9 + 9 = 27."},
            {"input": "10001", "expected_output": "2", "explanation": "1 + 0 + 0 + 0 + 1 = 2."},
            {"input": "5", "expected_output": "5", "explanation": "Single digit sum is 5."},
        ],
    },
    {
        "title": "Count Digits",
        "slug": "count-digits",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Count and print the total number of digits in a given non-negative integer `N`.\n"
            "Special case: The number 0 has exactly one digit.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print the total count of digits in `N`."
        ),
        "constraints": "0 <= N <= 10^12",
        "examples": [
            {"input": "12345", "expected_output": "5", "explanation": "12345 has 5 digits."},
            {"input": "0", "expected_output": "1", "explanation": "0 has 1 digit."},
            {"input": "7", "expected_output": "1", "explanation": "7 has 1 digit."},
            {"input": "100000", "expected_output": "6", "explanation": "100000 has 6 digits."},
            {"input": "9876543210", "expected_output": "10", "explanation": "10-digit number."},
        ],
    },
    {
        "title": "GCD of Two Numbers",
        "slug": "gcd-of-two-numbers",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Calculate the Greatest Common Divisor (GCD) of two non-negative integers `A` and `B`.\n\n"
            "### Input Format\n"
            "- Line 1: Two space-separated integers `A` and `B`.\n\n"
            "### Output Format\n"
            "- Print the greatest common divisor of `A` and `B`."
        ),
        "constraints": "0 <= A, B <= 10^9 (at least one is non-zero)",
        "examples": [
            {"input": "12 18", "expected_output": "6", "explanation": "The greatest common divisor of 12 and 18 is 6."},
            {"input": "20 5", "expected_output": "5", "explanation": "5 divides both 20 and 5."},
            {"input": "17 13", "expected_output": "1", "explanation": "Both are prime numbers, so gcd is 1."},
            {"input": "0 45", "expected_output": "45", "explanation": "gcd(0, 45) = 45."},
            {"input": "100 100", "expected_output": "100", "explanation": "gcd(100, 100) = 100."},
        ],
    },
    {
        "title": "LCM of Two Numbers",
        "slug": "lcm-of-two-numbers",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Calculate the Least Common Multiple (LCM) of two non-negative integers `A` and `B`.\n"
            "If either integer is 0, the LCM is 0.\n\n"
            "### Input Format\n"
            "- Line 1: Two space-separated integers `A` and `B`.\n\n"
            "### Output Format\n"
            "- Print the least common multiple of `A` and `B`."
        ),
        "constraints": "0 <= A, B <= 10^6",
        "examples": [
            {"input": "4 6", "expected_output": "12", "explanation": "LCM of 4 and 6 is 12."},
            {"input": "5 7", "expected_output": "35", "explanation": "LCM of coprime numbers 5 and 7 is 35."},
            {"input": "0 8", "expected_output": "0", "explanation": "If either number is 0, LCM is 0."},
            {"input": "15 20", "expected_output": "60", "explanation": "LCM of 15 and 20 is 60."},
            {"input": "12 12", "expected_output": "12", "explanation": "LCM of identical numbers is the number itself."},
        ],
    },
    {
        "title": "Even or Odd",
        "slug": "even-or-odd",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Determine whether a given integer `N` is even or odd.\n"
            "Support positive, negative, and zero values.\n\n"
            "### Input Format\n"
            "- Line 1: An integer `N`.\n\n"
            "### Output Format\n"
            "- Print `Even` if `N` is even, or `Odd` if `N` is odd."
        ),
        "constraints": "-10^9 <= N <= 10^9",
        "examples": [
            {"input": "4", "expected_output": "Even", "explanation": "4 is divisible by 2."},
            {"input": "7", "expected_output": "Odd", "explanation": "7 is not divisible by 2."},
            {"input": "0", "expected_output": "Even", "explanation": "0 is divisible by 2."},
            {"input": "-3", "expected_output": "Odd", "explanation": "-3 is odd."},
            {"input": "-18", "expected_output": "Even", "explanation": "-18 is even."},
        ],
    },
    {
        "title": "Leap Year",
        "slug": "leap-year",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Determine whether a given year `Y` is a leap year under the Gregorian calendar:\n"
            "1. Divisible by 4, and\n"
            "2. Not divisible by 100, unless\n"
            "3. Divisible by 400.\n\n"
            "### Input Format\n"
            "- Line 1: A positive integer `Y`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if `Y` is a leap year, or `No` otherwise."
        ),
        "constraints": "1 <= Y <= 10^5",
        "examples": [
            {"input": "2024", "expected_output": "Yes", "explanation": "2024 is divisible by 4 and not by 100."},
            {"input": "1900", "expected_output": "No", "explanation": "1900 is divisible by 100 but not by 400."},
            {"input": "2000", "expected_output": "Yes", "explanation": "2000 is divisible by 400."},
            {"input": "2023", "expected_output": "No", "explanation": "2023 is not divisible by 4."},
            {"input": "1600", "expected_output": "Yes", "explanation": "1600 is divisible by 400."},
        ],
    },
    {
        "title": "Multiplication Table",
        "slug": "multiplication-table",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Given two integers `N` and `M`, print the first `M` multiples of `N` "
            "(i.e., N * 1, N * 2, ..., N * M) separated by spaces on a single line.\n\n"
            "### Input Format\n"
            "- Line 1: Two space-separated integers `N` and `M`.\n\n"
            "### Output Format\n"
            "- Print the `M` multiples separated by spaces on a single line."
        ),
        "constraints": "1 <= N <= 1000\n1 <= M <= 100",
        "examples": [
            {"input": "5 4", "expected_output": "5 10 15 20", "explanation": "Multiples of 5 from 1 to 4."},
            {"input": "7 1", "expected_output": "7", "explanation": "First multiple of 7."},
            {"input": "3 5", "expected_output": "3 6 9 12 15", "explanation": "Multiples of 3 from 1 to 5."},
            {"input": "10 3", "expected_output": "10 20 30", "explanation": "Multiples of 10 from 1 to 3."},
            {"input": "1 6", "expected_output": "1 2 3 4 5 6", "explanation": "Multiples of 1 from 1 to 6."},
        ],
    },
    {
        "title": "Perfect Number",
        "slug": "perfect-number",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Determine whether a given positive integer `N` is a perfect number.\n"
            "A perfect number is a positive integer that is equal to the sum of its positive proper divisors "
            "(all positive divisors excluding `N` itself).\n\n"
            "### Input Format\n"
            "- Line 1: A positive integer `N`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if `N` is a perfect number, or `No` otherwise."
        ),
        "constraints": "1 <= N <= 10^7",
        "examples": [
            {"input": "6", "expected_output": "Yes", "explanation": "Proper divisors of 6 are 1, 2, 3: 1 + 2 + 3 = 6."},
            {"input": "28", "expected_output": "Yes", "explanation": "Proper divisors are 1, 2, 4, 7, 14: sum = 28."},
            {"input": "12", "expected_output": "No", "explanation": "Proper divisors are 1, 2, 3, 4, 6: sum = 16 != 12."},
            {"input": "1", "expected_output": "No", "explanation": "1 has no proper divisors."},
            {"input": "496", "expected_output": "Yes", "explanation": "496 is a perfect number."},
        ],
    },
    {
        "title": "Strong Number",
        "slug": "strong-number",
        "difficulty": "Easy",
        "tags": ["Math", "Basic Programming"],
        "description": (
            "Determine whether a given positive integer `N` is a Strong Number.\n"
            "A Strong Number is an integer where the sum of the factorials of its individual digits "
            "equals the number itself.\n\n"
            "### Input Format\n"
            "- Line 1: A positive integer `N`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if `N` is a Strong Number, or `No` otherwise."
        ),
        "constraints": "1 <= N <= 10^6",
        "examples": [
            {"input": "145", "expected_output": "Yes", "explanation": "1! + 4! + 5! = 1 + 24 + 120 = 145."},
            {"input": "1", "expected_output": "Yes", "explanation": "1! = 1."},
            {"input": "2", "expected_output": "Yes", "explanation": "2! = 2."},
            {"input": "123", "expected_output": "No", "explanation": "1! + 2! + 3! = 1 + 2 + 6 = 9 != 123."},
            {"input": "40585", "expected_output": "Yes", "explanation": "4! + 0! + 5! + 8! + 5! = 24 + 1 + 120 + 40320 + 120 = 40585."},
        ],
    },
    {
        "title": "Decimal to Binary",
        "slug": "decimal-to-binary",
        "difficulty": "Medium",
        "tags": ["Math", "String"],
        "description": (
            "Convert a given non-negative decimal integer `N` into its binary representation.\n"
            "Do not use Python's built-in `bin()` function.\n"
            "Print the binary representation without unnecessary leading zeros.\n"
            "If `N` is 0, output `0`.\n\n"
            "### Input Format\n"
            "- Line 1: A non-negative integer `N`.\n\n"
            "### Output Format\n"
            "- Print the binary representation of `N`."
        ),
        "constraints": "0 <= N <= 10^9",
        "examples": [
            {"input": "10", "expected_output": "1010", "explanation": "10 in binary is 1010."},
            {"input": "0", "expected_output": "0", "explanation": "0 in binary is 0."},
            {"input": "1", "expected_output": "1", "explanation": "1 in binary is 1."},
            {"input": "255", "expected_output": "11111111", "explanation": "255 in binary."},
            {"input": "64", "expected_output": "1000000", "explanation": "64 in binary."},
        ],
    },
    {
        "title": "Count Vowels and Consonants",
        "slug": "count-vowels-and-consonants",
        "difficulty": "Medium",
        "tags": ["String"],
        "description": (
            "Given a line of text, count the total number of vowels ('a', 'e', 'i', 'o', 'u') and consonants.\n"
            "- Treat uppercase and lowercase letters identically.\n"
            "- Ignore spaces, digits, and special characters.\n\n"
            "### Input Format\n"
            "- Line 1: A string of text.\n\n"
            "### Output Format\n"
            "- Print the vowel count and consonant count separated by a space: `<vowels> <consonants>`."
        ),
        "constraints": "1 <= text.length <= 10^4",
        "examples": [
            {"input": "Hello World", "expected_output": "3 7", "explanation": "Vowels: e, o, o (3). Consonants: H, l, l, W, r, l, d (7)."},
            {"input": "aeiou", "expected_output": "5 0", "explanation": "All 5 are vowels."},
            {"input": "Python 3.14!", "expected_output": "1 5", "explanation": "Vowels: o (1). Consonants: P, y, t, h, n (5). Digits/symbols ignored."},
            {"input": "12345 @#$", "expected_output": "0 0", "explanation": "No alphabetic letters present."},
            {"input": "TraceBack", "expected_output": "3 6", "explanation": "Vowels: a, e, a (3). Consonants: T, r, c, B, c, k (6)."},
        ],
    },
    {
        "title": "Palindrome String",
        "slug": "palindrome-string",
        "difficulty": "Medium",
        "tags": ["String", "Two Pointers"],
        "description": (
            "Check whether a given string is a palindrome.\n"
            "When checking, ignore all spaces and ignore letter case differences.\n\n"
            "### Input Format\n"
            "- Line 1: A string `s`.\n\n"
            "### Output Format\n"
            "- Print `Yes` if the string is a palindrome, or `No` otherwise."
        ),
        "constraints": "1 <= s.length <= 10^4",
        "examples": [
            {"input": "Race car", "expected_output": "Yes", "explanation": "Ignoring case and spaces, 'racecar' is a palindrome."},
            {"input": "hello", "expected_output": "No", "explanation": "'hello' reversed is 'olleh'."},
            {"input": "A Santa at NASA", "expected_output": "Yes", "explanation": "Ignoring case and spaces reads the same backward."},
            {"input": "madam", "expected_output": "Yes", "explanation": "'madam' is a palindrome."},
            {"input": "TraceBack", "expected_output": "No", "explanation": "'TraceBack' is not a palindrome."},
        ],
    },
    {
        "title": "Second Largest Distinct Element",
        "slug": "second-largest-distinct-element",
        "difficulty": "Medium",
        "tags": ["Array"],
        "description": (
            "Given an array of integers, find the second-largest DISTINCT element.\n"
            "If a second distinct element does not exist (e.g. all elements are identical or array length is less than 2), "
            "print `-1`.\n\n"
            "### Input Format\n"
            "- Line 1: An integer `N`, the number of elements in the array.\n"
            "- Line 2: `N` space-separated integers representing the array.\n\n"
            "### Output Format\n"
            "- Print the second-largest distinct element, or `-1` if none exists."
        ),
        "constraints": "1 <= N <= 10^5\n-10^9 <= nums[i] <= 10^9",
        "examples": [
            {"input": "5\n12 35 1 10 34 1", "expected_output": "34", "explanation": "Largest is 35, second largest distinct is 34."},
            {"input": "3\n10 10 10", "expected_output": "-1", "explanation": "All elements are equal; no second distinct element."},
            {"input": "1\n50", "expected_output": "-1", "explanation": "Array has only 1 element."},
            {"input": "4\n5 1 2 4", "expected_output": "4", "explanation": "Largest is 5, second largest is 4."},
            {"input": "4\n-10 -5 -2 -1", "expected_output": "-2", "explanation": "Largest is -1, second largest distinct is -2."},
        ],
    },
    {
        "title": "Missing Number in an Array",
        "slug": "missing-number-in-an-array",
        "difficulty": "Medium",
        "tags": ["Array", "Math"],
        "description": (
            "You are given an integer `N` and an array containing `N-1` distinct integers from the range 1 to `N`.\n"
            "Exactly one number is missing. Find and print the missing number.\n\n"
            "### Input Format\n"
            "- Line 1: An integer `N`, representing the range 1 to `N`.\n"
            "- Line 2: `N-1` space-separated integers representing the array elements.\n\n"
            "### Output Format\n"
            "- Print the single missing integer."
        ),
        "constraints": "2 <= N <= 10^5",
        "examples": [
            {"input": "5\n1 2 4 5", "expected_output": "3", "explanation": "Range is 1..5. 3 is missing."},
            {"input": "2\n1", "expected_output": "2", "explanation": "Range is 1..2. 2 is missing."},
            {"input": "2\n2", "expected_output": "1", "explanation": "Range is 1..2. 1 is missing."},
            {"input": "6\n6 3 2 4 1", "expected_output": "5", "explanation": "Range is 1..6. 5 is missing."},
            {"input": "4\n1 2 3", "expected_output": "4", "explanation": "Range is 1..4. 4 is missing."},
        ],
    },
]


def seed_problems(db: Optional[Session] = None) -> List[Problem]:
    """
    Idempotently insert or update initial DSA problems in the database.
    Checks each problem by slug and ensures complete-program mode examples are present.
    Never truncates or drops user tables.
    """
    should_close = False
    session = db
    if session is None:
        init_db()
        session = SessionLocal()
        should_close = True

    seeded_records: List[Problem] = []

    try:
        for p_data in INITIAL_PROBLEMS:
            slug = p_data["slug"]
            existing = session.query(Problem).filter(Problem.slug == slug).first()

            if existing is not None:
                existing.description = p_data["description"]
                existing.constraints = p_data.get("constraints", "")
                existing.difficulty = p_data["difficulty"]
                existing.tags = p_data.get("tags", [])
                
                # Refresh examples to complete-program format
                session.query(ProblemExample).filter(ProblemExample.problem_id == existing.id).delete()
                for ex in p_data.get("examples", []):
                    example = ProblemExample(
                        problem_id=existing.id,
                        input=ex["input"],
                        expected_output=ex["expected_output"],
                        explanation=ex.get("explanation"),
                    )
                    session.add(example)
                session.commit()
                session.refresh(existing)
                seeded_records.append(existing)
                continue

            # Create new Problem
            problem = Problem(
                title=p_data["title"],
                slug=p_data["slug"],
                description=p_data["description"],
                difficulty=p_data["difficulty"],
                constraints=p_data.get("constraints", ""),
                tags=p_data.get("tags", []),
            )
            session.add(problem)
            session.flush()  # Flush to obtain problem.id

            # Create associated public sample examples
            for ex in p_data.get("examples", []):
                example = ProblemExample(
                    problem_id=problem.id,
                    input=ex["input"],
                    expected_output=ex["expected_output"],
                    explanation=ex.get("explanation"),
                )
                session.add(example)

            session.commit()
            session.refresh(problem)
            seeded_records.append(problem)

        return seeded_records
    finally:
        if should_close:
            session.close()


if __name__ == "__main__":
    print("[*] Initializing database and running idempotent seed...")
    results = seed_problems()
    print(f"[+] Seeding complete. Total available seed problems: {len(results)}")
    for p in results:
        print(f"    - [{p.id}] {p.title} ({p.difficulty}) | slug: {p.slug} | examples: {len(p.examples)}")
