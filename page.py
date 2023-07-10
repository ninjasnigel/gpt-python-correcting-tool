import streamlit as st
import os

from script.correction import *
from script.gpt import *
from script.tests import *
from pagetexts import *

# Create a header menu with selectbox for page navigation
pages = ["Home", "File Selection", "Run Tests", "Test Results"]
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

else:
    st.title("About Page")
    st.write("Information about this app.")
