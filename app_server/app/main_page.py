import streamlit as st

from .base import BasePage
from .main import ComponentSState
from .components import HomeComponent, WakeupComponent, ChatRoomComponent
from model import COMPONENT_TYPE_TABLE


class MainPage(BasePage):
    @staticmethod
    def get_title() -> str:
        return "ChatGPT Demo"

    @staticmethod
    def get_icon() -> str:
        return "🧠"

    @staticmethod
    def init() -> None:
        ComponentSState.init()

    @staticmethod
    def main() -> None:
        current_component_entity = ComponentSState.get()
        if current_component_entity == COMPONENT_TYPE_TABLE.get_wake_up_entity():
            WakeupComponent.display()
        elif current_component_entity == COMPONENT_TYPE_TABLE.get_chat_room_entity():
            ChatRoomComponent.display()
        else:
            HomeComponent.display()

        # selected_page_entity = st.sidebar.selectbox(
        #     label="Pages Selection",
        #     options=COMPONENT_TYPE_TABLE.get_all_entities(),
        #     format_func=lambda x: x.label_en,
        #     key="PageSelectBox",
        # )
