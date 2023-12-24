from textwrap import dedent

import streamlit as st

from .. import BaseComponent


class HomeComponent(BaseComponent):
    @classmethod
    def init(cls) -> None:
        pass

    @classmethod
    def main(cls) -> None:
        content = dedent(
            f"""
            ### 🏠 Home  
            
            #### Overview
            Welcome to demo site of OpenAI API 🤖  
            Let's enjoy some functions 👏  

            #### Creators  
            - Takanari Shimbo 🦥  
            """
        )
        st.markdown(content)
