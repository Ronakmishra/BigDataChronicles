import streamlit as st
from utils import (
    load_metadata,
    get_openai_response,
    save_feedback,
    compare_answers,
    visualize_feedback
)

# Title of the app
st.title("GAIA Model Evaluation Tool")

# Load the GAIA dataset
data = load_metadata("metadata.jsonl")
test_cases = {item["task_id"]: item for item in data}

# Test case selection
selected_id = st.selectbox("Select a Test Case", options=list(test_cases.keys()))
test_case = test_cases[selected_id]

# Display test case details
st.subheader("Context")
st.write(test_case["Annotator Metadata"]["Steps"])

st.subheader("Question")
st.write(test_case["Question"])

# Evaluate the test case with OpenAI
if st.button("Evaluate with OpenAI"):
    # Generate OpenAI response
    response = get_openai_response(test_case["Annotator Metadata"]["Steps"], test_case["Question"])
    st.subheader("OpenAI Response")
    st.write(response)

    st.subheader("Ground Truth Answer")
    st.write(test_case["Final answer"])

    # Compare OpenAI response with the ground truth
    if compare_answers(response, test_case["Final answer"]):
        st.success("Validation Approved! The response matches the ground truth.")
    else:
        st.error("Validation Disapproved! The response does not match the ground truth.")

    # Allow users to provide feedback
    feedback = st.text_input("Provide Feedback:")
    if st.button("Submit Feedback"):
        save_feedback(test_case["task_id"], response, feedback)
        st.success("Feedback recorded!")

# Visualize feedback
st.header("Feedback Summary")
visualize_feedback()

data = load_metadata("metadata.jsonl")  # Replace "metadata.jsonl" with the actual path
print(data[:2])  # Print the first 2 test cases
