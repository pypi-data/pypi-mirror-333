import streamlit as st
from editors.feature_view_editor_ui import FeatureEditorState
from editors import feature_view_editor_ui  # Import the module with our function

# Your existing app setup
st.set_page_config(page_title="My Main App", layout="wide")
st.title("My Main Application")

# Your existing content...

st.session_state['editor_state'] = st.session_state.get('editor_state', FeatureEditorState())

# Embed the Tecton Feature Creator where needed
col1, col2 = st.columns(2)
with col1:
    generated_code = feature_view_editor_ui.display_editor(
        key_prefix="tecton_editor",
        state=st.session_state['editor_state']
    )

    if generated_code:
        # Do something with the generated code if needed
        st.session_state.last_generated_code = generated_code
