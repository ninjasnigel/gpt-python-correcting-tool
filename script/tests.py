def test(func):
    errors = []

    # Define test cases as (input, expected_output, error_message) tuples
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
    for input_value, expected_output, error_message in test_cases:
        try:
            # Assert if the output is as expected
            assert func(input_value) == expected_output, error_message
        except AssertionError as e:
            # Append the error message to the list
            errors.append(str(e))

    return errors
