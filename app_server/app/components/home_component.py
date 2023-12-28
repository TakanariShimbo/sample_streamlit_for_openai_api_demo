from textwrap import dedent

import streamlit as st
from streamlit_lottie import st_lottie_spinner

from ..base import BaseComponent
from ..s_states import CreateProcesserSState, EnterProcesserSState
from controller import LottieManager
from model import ChatRoomTable, DATABASE_ENGINE


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        CreateProcesserSState.init()
        EnterProcesserSState.init()

    @classmethod
    def main(cls) -> None:
        """
        TITLE AND OVERVIEW
        """
        content = dedent(
            f"""
            ### 🏠 Home
            
            #### Overview
            Welcome to demo site of ChatGPT.   
            Experience the forefront of AI technology and explore the possibilities of the future.  
            AI makes your daily life smarter and easier.  
            """
        )

        st.markdown(content)

        """
        CREATE FORM
        """
        st.markdown("#### Create Room")
        with st.form(key="CreateForm", border=True):
            inputed_title = st.text_input(
                label="Title",
                placeholder="Input room title here.",
                key="RoomTitleTextInput",
            )
            create_message_area = st.empty()
            _, button_area, _ = st.columns([5, 3, 5])
            with button_area:
                is_create_pushed = st.form_submit_button(label="CREATE", type="primary", use_container_width=True)
            _, create_loading_area, _ = st.columns([1, 1, 1])

        """
        ENTER FORMS
        """
        left, right = st.columns([1, 1])
        with left:
            N = 5
            selected_room_entity = None
            selected_enter_loading_area = None
            st.markdown("#### Enter Room")
            chat_room_table = ChatRoomTable.load_from_database(database_engine=DATABASE_ENGINE)
            for i, chat_room_entity in enumerate(chat_room_table.get_all_entities()[::-1][:N]):
                with st.container(border=True):
                    st.markdown(f"###### 📝 {chat_room_entity.title}")
                    _, enter_loading_area, _ = st.columns([1, 2, 1])
                    _, button_area = st.columns([5, 1])
                    with button_area:
                        is_enter_pushed = st.button(label="🚪", key=f"RoomEnterButton{i}", use_container_width=True)
                    if is_enter_pushed:
                        selected_room_entity = chat_room_entity
                        selected_enter_loading_area = enter_loading_area

        """
        CREATE PROCESS
        """
        if is_create_pushed:
            with create_loading_area:
                with st_lottie_spinner(animation_source=LottieManager.LOADING):
                    is_success = CreateProcesserSState.on_click_run(
                        message_area=create_message_area,
                        title=inputed_title,
                    )
                if is_success:
                    cls.deinit()
                    st.rerun()

        """
        ENTER PROCESS
        """
        if selected_room_entity and selected_enter_loading_area:
            with selected_enter_loading_area:
                with st_lottie_spinner(animation_source=LottieManager.LOADING):
                    is_success = EnterProcesserSState.on_click_run(room_id=selected_room_entity.room_id)
                if is_success:
                    cls.deinit()
                    st.rerun()

    @staticmethod
    def deinit() -> None:
        CreateProcesserSState.deinit()
