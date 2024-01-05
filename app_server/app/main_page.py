from .base import BasePage
from .main_s_states import MainComponentSState
from .main_components import WakeupComponent, SignInComponent, HomeComponent, ChatRoomComponent
from model import MAIN_COMPONENT_TYPE_TABLE


class MainPage(BasePage):
    @staticmethod
    def get_title() -> str:
        return "ChatGPT"

    @staticmethod
    def get_icon() -> str:
        return "🧠"

    @staticmethod
    def init() -> None:
        MainComponentSState.init()

    @staticmethod
    def main() -> None:
        current_component_entity = MainComponentSState.get()
        if current_component_entity == MAIN_COMPONENT_TYPE_TABLE.get_wake_up_entity():
            WakeupComponent.run()
        elif current_component_entity == MAIN_COMPONENT_TYPE_TABLE.get_sign_in_entity():
            SignInComponent.run()
        elif current_component_entity == MAIN_COMPONENT_TYPE_TABLE.get_home_entity():
            HomeComponent.run()
        elif current_component_entity == MAIN_COMPONENT_TYPE_TABLE.get_chat_room_entity():
            ChatRoomComponent.run()
        else:
            raise ValueError("ComponentSState Value Error")
