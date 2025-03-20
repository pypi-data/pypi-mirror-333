# streamlit-session-manager

this component allows you to manager you session storage

## Installation instructions 

```sh
pip install streamlit-session-manager
```

## Usage instructions

```python
import streamlit as st

from streamlit_session_manager import streamlit_session_manager

value = streamlit_session_manager()

st.write(value)
