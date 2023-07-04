#import all modules from for_correction
import for_correction.code1
import for_correction.code2
import for_correction.code3
from tests.tests import test

import os
import importlib.util
import traceback
from script.gpt import get_gpt_feedback

pass_str = "Student code passed all tests!: "
fail_str = "Student code failed one or more tests: "
crash_str = "Student code crashed when running tests, the following error was printed: "

def main():
    return False

if __name__ == "__main__":
    main()


# This is your test function
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

# Directory containing student code
directory = "for_correction"
context_dir = "assignment.txt"


import os
import importlib.util
import traceback

# Loop through each file in the directory
for filename in os.listdir(directory):
    # Only process .py files
    if filename.endswith(".py"):
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
            continue

        # Get the multiply function from the module
        multiply_func = getattr(module, "multiply", None)
        
        context = get_context(context_dir)
        feedback_str = context +"\n\n Student code: \n\n" +code_text + "\n\n Test results: \n"
        if callable(multiply_func):
            with open('corrected/' + filename[:-3] + '.md', "w") as file:
                # Call your test function and save the result
                try:
                    result = run_tests(multiply_func, test)
                    feedback_str += f"{filename}: {result}\n"
                except Exception as e:
                    feedback_str += f"{filename}: {crash_str + str(e)}\n"
                
                # Get feedback from GPT-3
                feedback_str += "\n GPT feedback: \n" + get_gpt_feedback(feedback_str)
                file.write(feedback_str[len(context)+3:])

        else:
            file.write(f"{filename} does not contain a 'multiply' function.\n")

