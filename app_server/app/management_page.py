import streamlit as st

from .base import BasePage


class ManagementPage(BasePage):
    @staticmethod
    def get_title() -> str:
        return "ChatGPT Management"

    @staticmethod
    def get_icon() -> str:
        return "🧠"

    @staticmethod
    def init() -> None:
        pass

    @staticmethod
    def main() -> None:
        st.markdown("## Management")