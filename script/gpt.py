import openai
openai.api_type = "azure"
openai.api_version = "2023-05-15"
GPT_MODEL_token = "gpt-3.5-turbo"
GPT_MODEL = "gpt-35-turbo"

try:
    with open('openai.base') as f:
        openai.api_base = f.read().strip()

    with open('openai.key') as f:
        openai.api_key = f.read().strip()
except: # Use streamlit secrets
    import streamlit as st
    openai.api_key = st.secrets["openai_key"]
    openai.api_base = st.secrets["openai_base"]
    
system_msg_old = "You provided with student code, the result of the test ran on the code, and the potential errors \
                        You are to aid a teacher in the grading of the coding assignement. You will do this by discussing \
                        what is good and what is bad in the student code. Explain what the student did right or wrong. \
                        List the good and bad things in bullet points. Discuss and comment the readability, efficiency, \
                        structure, and style of the code in these bullet points. Feel free to mention other relevant things.  \
                        Do not give any suggestions on how to improve the code. IMPORTANT: add #### before each bullet point. "

json_msg = "You provided with student code, the result of the test ran on the code, and the potential errors \
                        You are to aid a teacher in the grading of the coding assignement. You will do this by discussing \
                        what is good and what is bad in the student code. Explain what the student did right or wrong. \
                        List the good and bad things in bullet points. Discuss and comment the readability, efficiency, \
                        structure, and style of the code in these bullet points. Feel free to mention other relevant things.  \
                        IMPORTANT: add #### before each bullet point. The bullet points should be in the following format: \
                        #### Good: #### Bad: #### Other:"


def get_gpt_feedback(feedback_str):
    system_msg = json_msg
    conversation = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": feedback_str}
    ]
    response = openai.ChatCompletion.create(
        engine=GPT_MODEL,
        messages=conversation
    )
    return response['choices'][0]['message']['content']