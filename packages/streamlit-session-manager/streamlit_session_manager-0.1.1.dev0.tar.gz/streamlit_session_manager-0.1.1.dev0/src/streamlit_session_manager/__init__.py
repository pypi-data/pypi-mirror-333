from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called streamlit_session_manager,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"streamlit_session_manager", path=str(frontend_dir)
)


# set item in you session state
def set_item(
    key: str,
    value: str,
    _action='set_item'
):
    return _component_func(
        key=key,
        value=value,
        action=_action
    )

def get_item(
    key: str,
    _action='get_item'
):
    return _component_func(
        key=key,
        action=_action
    )
