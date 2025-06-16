import streamlit as st

def make_side_bar():
    """
    Creates a sidebar in the Streamlit app for customizing large language model (LLM) settings.

    Returns:
        dict: A dictionary containing the following keys and their selected values:
            - 'model' (str): Selected model name.
            - 'memory_length' (int): Number of past messages to remember.
            - 'temperature' (float): Randomness level for response generation.
            - 'top_p' (float): Top-p value for nucleus sampling.
            - 'max_tokens' (int): Maximum tokens in the response. 
    """
    st.sidebar.title('Customization Panel')

    # Model selection
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama3-70b-8192', 'compound-beta', 'gpt-4', 'mistral-7b', 'gemma-7b']
    )

    # Memory settings
    memory_length = st.sidebar.slider(
        'Conversational memory length (number of past turns to remember)',
        1, 20, value=5
    )

    # Temperature control
    temperature = st.sidebar.slider(
        'Temperature (controls randomness)',
        0.0, 1.5, value=0.7, step=0.1
    )

    # Top-p (nucleus sampling)
    top_p = st.sidebar.slider(
        'Top-p (nucleus sampling)',
        0.0, 1.0, value=0.9, step=0.05
    )

    # Max tokens
    max_tokens = st.sidebar.slider(
        'Maximum tokens in response',
        50, 8192, value=512, step=50
    )

    # Streaming toggle
    streaming = st.sidebar.checkbox('Enable streaming response', value=True)

    # Return all the settings
    return {
        'model': model,
        'memory_length': memory_length,
        'temperature': temperature,
        'top_p': top_p,
        'max_tokens': max_tokens,
        'streaming': streaming
    }
