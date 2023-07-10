def multiply(str):
    product = 1
    for char in str:
        if char.isdigit():
            product *= int(char)
    
    divided_by_three = int(str) / 3
    
    return product > divided_by_three