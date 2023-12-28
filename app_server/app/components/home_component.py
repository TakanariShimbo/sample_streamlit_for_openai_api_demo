from textwrap import dedent
from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_lottie import st_lottie_spinner

from ..base import BaseComponent
from ..s_states import CreateProcesserSState, EnterProcesserSState
from controller import LottieManager
from model import ChatRoomTable, ChatRoomEntity, DATABASE_ENGINE


class CreateActionResults:
    def __init__(
        self,
        title: str,
        message_area: DeltaGenerator,
        loading_area: DeltaGenerator,
        is_pushed: bool,
    ) -> None:
        self._title = title
        self._message_area = message_area
        self._loading_area = loading_area
        self._is_pushed = is_pushed

    @property
    def title(self):
        return self._title

    @property
    def message_area(self):
        return self._message_area

    @property
    def loading_area(self):
        return self._loading_area

    @property
    def is_pushed(self):
        return self._is_pushed


class EditActionResults:
    def __init__(
        self,
        chat_room_entity: ChatRoomEntity,
        loading_area: DeltaGenerator,
    ) -> None:
        self._chat_room_entity = chat_room_entity
        self._loading_area = loading_area

    @property
    def chat_room_entity(self):
        return self._chat_room_entity

    @property
    def loading_area(self):
        return self._loading_area


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        CreateProcesserSState.init()
        EnterProcesserSState.init()

    @staticmethod
    def _display_title() -> None:
        st.markdown("### 🏠 Home")

    @staticmethod
    def _display_overview() -> None:
        content = dedent(
            f"""
            #### Overview
            Welcome to demo site of ChatGPT.   
            Experience the forefront of AI technology and explore the possibilities of the future.  
            AI makes your daily life smarter and easier.  
            """
        )
        st.markdown(content)

    @staticmethod
    def _display_create_form_and_get_results() -> CreateActionResults:
        st.markdown("#### Create Room")
        with st.form(key="CreateForm", border=True):
            inputed_title = st.text_input(
                label="Title",
                placeholder="Input room title here.",
                key="RoomTitleTextInput",
            )
            message_area = st.empty()
            _, button_area, _ = st.columns([5, 3, 5])
            with button_area:
                is_pushed = st.form_submit_button(label="CREATE", type="primary", use_container_width=True)
            _, loading_area, _ = st.columns([1, 1, 1])

        return CreateActionResults(
            title=inputed_title,
            message_area=message_area,
            loading_area=loading_area,
            is_pushed=is_pushed,
        )

    @staticmethod
    def _display_editables_and_get_results() -> Optional[EditActionResults]:
        N = 5
        selected_chat_room_entity = None
        selected_loading_area = None
        st.markdown("#### Enter Room")
        chat_room_table = ChatRoomTable.load_from_database(database_engine=DATABASE_ENGINE)
        for i, chat_room_entity in enumerate(chat_room_table.get_all_entities()[::-1][:N]):
            with st.container(border=True):
                contents = dedent(
                    f"""
                    ###### 📝 {chat_room_entity.title}  
                    👤 {chat_room_entity.account_id}   
                    🕛 {chat_room_entity.created_at}
                    """
                )
                st.markdown(contents)

                _, loading_area, _ = st.columns([1, 2, 1])
                _, button_area = st.columns([5, 1])
                with button_area:
                    is_pushed = st.button(label="🚪", key=f"RoomEnterButton{i}", use_container_width=True)
                if is_pushed:
                    selected_chat_room_entity = chat_room_entity
                    selected_loading_area = loading_area

        if selected_chat_room_entity == None:
            return None
        if selected_loading_area == None:
            return None

        return EditActionResults(
            chat_room_entity=selected_chat_room_entity,
            loading_area=selected_loading_area,
        )

    @staticmethod
    def _execute_create_process(create_action_results: CreateActionResults) -> bool:
        if not create_action_results.is_pushed:
            return False

        with create_action_results.loading_area:
            with st_lottie_spinner(animation_source=LottieManager.LOADING):
                is_success = CreateProcesserSState.on_click_run(
                    message_area=create_action_results.message_area,
                    title=create_action_results.title,
                )
        return is_success

    @staticmethod
    def _execute_edit_process(edit_action_results: Optional[EditActionResults]) -> bool:
        if not edit_action_results:
            return False

        with edit_action_results.loading_area:
            with st_lottie_spinner(animation_source=LottieManager.LOADING):
                is_success = EnterProcesserSState.on_click_run(room_id=edit_action_results.chat_room_entity.room_id)

        return is_success

    @classmethod
    def main(cls) -> None:
        cls._display_title()
        cls._display_overview()

        create_action_results = cls._display_create_form_and_get_results()

        left, right = st.columns([1, 1])
        with left:
            edit_action_results = cls._display_editables_and_get_results()

        is_success = cls._execute_create_process(create_action_results=create_action_results)
        if is_success:
            cls.deinit()
            st.rerun()

        is_success = cls._execute_edit_process(edit_action_results=edit_action_results)
        if is_success:
            cls.deinit()
            st.rerun()

    @staticmethod
    def deinit() -> None:
        CreateProcesserSState.deinit()
        EnterProcesserSState.deinit()
