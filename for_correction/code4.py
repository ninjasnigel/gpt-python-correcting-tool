def fix_str(num):
    fixed_str = ""
    for char in str(num):
        if not char.isdigit():
            continue
        else:
            fixed_str += char
    if not fixed_str:
        return '0'
    return fixed_str

def multiply_digits(num):
    multiplied = 1
    for digit in num:
        multiplied *= int(digit)
    return multiplied

def multiply(num_str):
    fixed_str = fix_str(num_str)
    if fixed_str:
        multiplied = multiply_digits(fixed_str)
    else: return False
    return multiplied > int(fixed_str)/3