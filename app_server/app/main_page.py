import streamlit as st

from .base import BasePage
from .s_states import ComponentSState
from .components import WakeupComponent, SignInComponent, HomeComponent, ChatRoomComponent
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
            WakeupComponent.run()
        elif current_component_entity == COMPONENT_TYPE_TABLE.get_sign_in_entity():
            SignInComponent.run()
        elif current_component_entity == COMPONENT_TYPE_TABLE.get_home_entity():
            HomeComponent.run()
        elif current_component_entity == COMPONENT_TYPE_TABLE.get_chat_room_entity():
            ChatRoomComponent.run()
        else:
            raise ValueError("ComponentSState Value Error")
