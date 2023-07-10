import streamlit as st
import os

from script.correction import *
from script.gpt import *
from script.tests import *
from pagetexts import *
import ast

# Create a header menu with selectbox for page navigation
pages = ["Home", "File Selection", "Run Tests", "Test Results", "Test Configuration"]
selected_page = st.selectbox("Choose a page", pages)
save_py_file_dir = "for_correction/"
corrected_dir = "corrected/"
delim = "#--#"

# Display content depending on selected page
if selected_page == "Home":
    st.title("Home Page")
    st.markdown(homepage_description)
    st.image("https://media.giphy.com/media/3o7aDcz6Yulr061Z9m/giphy.gif")

elif selected_page == "File Selection":
    st.title("File Selection Page")
    
    # File uploader
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=['py'])

    # Check if files are uploaded and store them in session state
    if uploaded_files:
        st.session_state['uploaded_files'] = uploaded_files
        
    # Display uploaded files from session state
    if 'uploaded_files' in st.session_state:
        for uploaded_file in st.session_state['uploaded_files']:
            st.write(f"You have uploaded {uploaded_file.name}")

            # Save uploaded file to directory
            with open(save_py_file_dir + uploaded_file.name, "wb") as file:
                file.write(uploaded_file.getbuffer())

elif selected_page == "Run Tests":
    st.title("Run Tests Page")

    # Button to trigger the tests
    if st.button("Run Tests"):
        st.write("Running tests...")
        files_for_correction = get_files_for_correction(save_py_file_dir)
        progress_bar = st.progress(0)
        # Create a placeholder for text
        status_text = st.empty()
        total_files = len(files_for_correction)
        for index, files in enumerate(files_for_correction):
            # Corrected progress percentage calculation
            progress_percentage = (index + 1) / total_files
            write_feedback_on_file(save_py_file_dir, files, test=test, save_dir=corrected_dir)
            
            # Update progress bar
            progress_bar.progress(progress_percentage)

            # Update text in the placeholder
            status_text.text(f"{index+1} out of {total_files} files processed.")

            # Print finished testing
        st.write("Finished running tests!")
        
        # Get list of markdown files
        markdown_files = [f for f in os.listdir(corrected_dir) if f.endswith(".md")]

        # Store markdown files in session state
        st.session_state['markdown_files'] = markdown_files

        if st.button("Results"):
            selected_page = "Test Results"

elif selected_page == "Test Results":
    st.title("Test Results Page")
    
    # List markdown files from the directory
    markdown_files = [f for f in os.listdir(corrected_dir) if f.endswith(".md")]
    
    # Check if markdown files are available
    if markdown_files:
        # Store markdown files in session state
        st.session_state['markdown_files'] = markdown_files
        
        # Selectbox for markdown files
        selected_markdown = st.selectbox("Choose a markdown file", st.session_state['markdown_files'])
        
        # Display the content of the selected markdown file
        with open(corrected_dir + selected_markdown, "r") as file:
            parts = file.read().split(delim)
            st.markdown(parts[0])
            st.code(parts[1], language="python")
            st.markdown(parts[2]) # md file extension
    else:
        st.write("No test results available yet.")

if selected_page == "Test Configuration":
    st.title("Test Configuration Page")

    # Text input for test configuration
    description_value = ""

    #if os.path.isfile("description.txt"):
    #    with open("description.txt", "r") as f:
    #        description_value = f.read()

    description = st.text_area("Enter your test configuration here:", value=description_value, height=200)

    # Initialize session_state if not already done
    if "test_count" not in st.session_state:
        st.session_state.test_count = 0
    if "tests" not in st.session_state:
        st.session_state.tests = {}

    # Load existing tests from file
    if os.path.isfile("test_cases.py"):
        with open("test_cases.py", "r") as f:
            lines = f.readlines()
            # Update test_count
            st.session_state.test_count = len(lines)
            for i, line in enumerate(lines):
                # Parse the test input and expected output
                test_input, expected_output = ast.literal_eval(line[line.find("(")+1:line.find(")")])
                # Store them in the session state
                st.session_state.tests[i] = {
                    "input": str(test_input),
                    "expected_output": str(expected_output)
                }

    # If button pressed, increment count
    if st.button("Add Test"):
        st.session_state.test_count += 1

    # Display text inputs for each test
    for i in range(st.session_state.test_count):
        with st.container():
            cols = st.columns(2)
            test_input = st.session_state.tests[i]["input"] if i in st.session_state.tests else ""
            expected_output = st.session_state.tests[i]["expected_output"] if i in st.session_state.tests else ""
            st.session_state.tests[i] = {
                "input": cols[0].text_input(f"Test {i+1} Input:", value=test_input),
                "expected_output": cols[1].text_input(f"Test {i+1} Expected Output:", value=expected_output)
            }

    # Add save configuration button
    if st.button("Save Configuration"):
        # Check if we have at least one test and description
        if st.session_state.test_count > 0 and description:
            # Save the inputs from the big text box to a string
            with open("description.txt", "w") as f:
                f.write(description)

            # Save tests as tuples
            with open("test_cases.py", "w") as f:
                for i in range(st.session_state.test_count):
                    input_ = safely_literal_eval(st.session_state.tests[i]["input"])
                    expected_output = safely_literal_eval(st.session_state.tests[i]["expected_output"])
                    f.write(f"test_{i} = ({input_}, {expected_output})\n")

            st.success("Configuration saved successfully!")
        else:
            st.error("Please ensure that a test is added and a description is written before saving.")