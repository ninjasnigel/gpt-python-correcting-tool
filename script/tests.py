from test_cases import *
import traceback

def load_tests_cases():
    # Load test cases from test_cases.py
    test_cases = []
    try:
        for i in range(100):
            test_cases.append(globals()[f"test_{i}"])
            print('loaded test case', i)
    except:
        pass
    return test_cases

def safely_literal_eval(input_string):
    import ast
    try:
        return ast.literal_eval(input_string)
    except (ValueError, SyntaxError):
        return repr(input_string)
    
def create_error_message(test_case):
    input_value, expected_output = test_case
    return f"Input {input_value} should return {expected_output}"

def test(func):
    errors = []
    test_cases = load_tests_cases()
    print('loaded test cases', test_cases)
    if not test_cases:
        test_cases = [
            (101, False, "Input 101 should return False"),
            (111, False, "Input 111 should return False"),
            (123, False, "Input 123 should return False"),
            (123456789, False, "Input 123456789 should return False"),
            (9999999999, True, "Input 9999999999 should return True"),
            (99, True, "Input 99 should return True"),
            ("3I33", False, "Input '3I33' should return False"),
            ("9hejärjagivägen?9", True, "Input '9hejärjagivägen?9' should return True"),
        ]

    # Loop through each test case
    for input_value, expected_output in test_cases:
        try:
            # Assert if the output is as expected
            assert func(input_value) == expected_output, create_error_message((input_value, expected_output))
        except AssertionError as e:
            # Append the error message to the list
            errors.append(traceback.format_exc().splitlines()[-1])

    return errors
