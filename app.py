import streamlit as st

from engine.validation import validate_inputs
from engine.prompt import (
    extract_constraints,
    is_output_required,
    build_final_prompt
)
from engine.llm import generate_code
from memory import init_db, store_generation, get_session_history

# Page Configuration
st.set_page_config(
    page_title="Code Generator",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Code Generator")
st.caption("Generates ONLY code")

# Session State Initialization
if "reset_input" not in st.session_state:
    st.session_state.reset_input = False

if "last_output" not in st.session_state:
    st.session_state.last_output = None

# Initialize Database
init_db()

# Sidebar – Session History
st.sidebar.title("📚 Session History")

history = get_session_history()
if history:
    for idx, record in enumerate(history):
        with st.sidebar.expander(f"Generation {idx + 1}"):

            st.markdown("**Final Prompt Sent to LLM:**")
            st.code(record["final_prompt"], language="text")

            st.markdown("**Generated Code:**")
            st.code(
                record["generated_code"],
                language=record["language"].lower()
            )
else:
    st.sidebar.info("No generations yet")

# Main Input Section
problem_statement = st.text_area(
    "Problem Statement",
    key="problem_input",
    value="" if st.session_state.reset_input else st.session_state.get("problem_input", ""),
    placeholder="e.g., Generate Fibonacci series in Python as a function"
)

# reset flag AFTER widget creation
st.session_state.reset_input = False

# Retrive Language, Code Format, Output Format from problem statement
constraints = extract_constraints(problem_statement)

# Language Selection
language = constraints["language"] or st.selectbox(
    "Programming Language *",
    ["", "Python", "Java", "C++", "JavaScript"]
)

# Code Format Selection
code_format = constraints["code_format"] or st.selectbox(
    "Code Format *",
    ["", "function", "class", "script", "method"]
)

# Output Format (Conditional)
output_needed = is_output_required(problem_statement)

output_format = None
if output_needed:
    output_format = constraints["output_format"] or st.selectbox(
        "Output Format *",
        ["", "series", "single value", "boolean", "list"]
    )

# Generate Button Logic
if st.button("Generate Code"):

    # Step 1: Validation
    error = validate_inputs(
        problem_statement,
        language,
        code_format,
        output_needed,
        output_format
    )

    if error:
        st.error(error)
        st.stop()

    # Step 2: Build FINAL prompt
    final_prompt = build_final_prompt(
        problem_statement,
        language,
        code_format,
        output_format
    )

    # Step 3: Generate Code (Quota-safe)
    with st.spinner("Generating code..."):
        try:
            generated_code = generate_code(final_prompt)
        except RuntimeError as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                st.warning(
                    "🚫 **API quota exceeded**\n\n"
                )
                st.stop()
            else:
                st.error(msg)
                st.stop()

    # Step 4: Store FINAL prompt + code in DB
    store_generation(
        problem=problem_statement,
        language=language,
        code_format=code_format,
        output_format=output_format or "N/A",
        final_prompt=final_prompt,
        generated_code=generated_code
    )

    # Step 5: Store output in session state
    st.session_state.last_output = {
        "language": language,
        "generated_code": generated_code,
        "final_prompt": final_prompt
    }

    # Step 6: Clear input safely
    st.session_state.reset_input = True
    st.rerun()

# Output Section (Persistent)
if st.session_state.last_output:

    st.subheader("✅ Generated Code")
    st.code(
        st.session_state.last_output["generated_code"],
        language=st.session_state.last_output["language"].lower()
    )
#conda activate C_Aenv