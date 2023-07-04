#test functions
#input 101 should return 0
def test(func):
    assert func(101) == False, "Input 101 should return False"
    assert func(111) == False, "Input 111 should return False"
    assert func(123) == False, "Input 123 should return False"
    assert func(123456789) == False, "Input 123456789 should return False"
    assert func(9999999999) == True, "Input 9999999999 should return True"
    assert func(99) == True, "Input 99 should return True"
    assert func("3I33") == False, "Input '13I5' should return False"
    assert func("9hejärjagivägen?9") == True, "Input '9hejärjagivägen?9' should return True"
    print("All tests passed!")