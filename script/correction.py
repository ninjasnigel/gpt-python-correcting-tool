import os
import importlib.util
import traceback
from script.gpt import *
from tests.tests import *

pass_str = "Student code :white_check_mark: **PASSED** :white_check_mark:  all tests! "
fail_str = "Student code :skull: **FAILED** :skull: one or more tests "
crash_str = "Student code :warning: **CRASHED** :warning: when running tests, the following error was printed: "
delim = "#--#"

# Directory containing student code
context_dir = "assignment.txt"

import os
import importlib.util
import traceback

def run_test_on_dir(directory, filename, test=test, save_dir="corrected/"):
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        # Only process .py files
        if filename.endswith(".py"):
            write_feedback_on_file(directory, filename, test=test, save_dir=save_dir)

def write_feedback_on_file(directory, filename, test=test, save_dir="corrected/"):
    # Create the path to the python file
    file_path = os.path.join(directory, filename)
    
    # Read the contents of the file as text
    with open(file_path, 'r') as code_file:
        code_text = code_file.read()

    # Load the module
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except:
        file.write(f"Error importing {filename}: {traceback.format_exc()}\n")
        return

    # Get the multiply function from the module
    multiply_func = getattr(module, "multiply", None)
    
    context = get_context(context_dir)
    feedback_str = context  +"\n\n ### Student code: \n\n" +delim +"\n" \
                            +code_text +"\n" +delim + "\n\n Test results: \n"
    if callable(multiply_func):
        with open(save_dir + filename[:-3] + '.md', "w") as file:
            # Call your test function and save the result
            try:
                result = run_tests(multiply_func, test)
                if result:
                    feedback_str += f'{pass_str} \n'
                else:
                    feedback_str += f'{fail_str} \n'
            except Exception as e:
                feedback_str += f'{crash_str}: {e} \n'
            
            # Get feedback from GPT-3
            feedback_str += "\n ### GPT feedback: \n" + get_gpt_feedback(feedback_str)
            file.write(feedback_str[len(context)+3:])

    else:
        file.write(f"{filename} does not contain a 'multiply' function.\n")

if __name__ == "__main__":
    run_test_on_dir()

def run_tests(student_func, test_func):
    try:
        test_func(student_func)
        return True
    except AssertionError as e:
        return False

def get_context(dir):
    with open(dir, 'r') as file:
        context = file.read()
    return context