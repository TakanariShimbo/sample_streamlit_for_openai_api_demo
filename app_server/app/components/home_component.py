from textwrap import dedent

import streamlit as st

from ..base import BaseComponent


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        pass

    @staticmethod
    def main() -> None:
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
