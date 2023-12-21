import streamlit as st

from . import BasePage, HomeComponent, WakeupComponent, ChatGptComponent
from model import PageTypeTable


class MainPage(BasePage):
    @classmethod
    def main(cls) -> None:
        WakeupComponent.display_and_rerun_only_first_time()

        selected_page_entity = st.sidebar.selectbox(
            label="Pages Selection",
            options=PageTypeTable.get_all_entities(),
            format_func=lambda x: x.label_en,
            key="PageSelectBox",
        )

        if selected_page_entity == PageTypeTable.get_chat_gpt_entity():
            ChatGptComponent.display()
        else:
            HomeComponent.display()
