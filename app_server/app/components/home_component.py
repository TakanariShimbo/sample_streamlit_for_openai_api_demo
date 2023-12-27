from textwrap import dedent

import streamlit as st
from streamlit_lottie import st_lottie_spinner

from ..base import BaseComponent
from ..s_states import CreateProcesserSState, ChatMessagesSState, ComponentSState
from controller import LottieManager, ChatMessagesManager
from model import ChatRoomTable, DATABASE_ENGINE


class HomeComponent(BaseComponent):
    @staticmethod
    def init() -> None:
        CreateProcesserSState.init()

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
        create_form = st.form(key="CreateForm", border=False)
        with create_form:
            st.markdown("#### Create Room")

            inputed_title = st.text_input(
                label="Title",
                placeholder="Input room title here.",
                key="RoomTitleTextInput",
            )

            message_area = st.empty()

            _, button_area, _ = st.columns([5, 3, 5])
            with button_area:
                is_create_pushed = st.form_submit_button(label="CREATE", type="primary", use_container_width=True)

            _, loading_area, _ = st.columns([1, 1, 1])

        """
        ENTER FORMS
        """
        N = 5
        selected_room_entity = None
        st.markdown("#### Enter Room")
        chat_room_table = ChatRoomTable.load_from_database(database_engine=DATABASE_ENGINE)
        for i, chat_room_entity in enumerate(chat_room_table.get_all_entities()[::-1][:N]):
            with st.container(border=True):
                title_area, button_area = st.columns([3, 1])
                title_area.markdown(f"##### 📝 {chat_room_entity.title}")
                is_pushed = button_area.button(label="ENTER", key=f"RoomEnterButton{i}", use_container_width=True)
                if is_pushed:
                    selected_room_entity = chat_room_entity
                

        """
        CREATE PROCESS
        """
        if is_create_pushed:
            with loading_area:
                with st_lottie_spinner(animation_source=LottieManager.LOADING):
                    is_success = CreateProcesserSState.on_click_run(
                        message_area=message_area,
                        title=inputed_title,
                    )
                if is_success:
                    cls.deinit()
                    st.rerun()

        """
        CREATE PROCESS
        """
        if selected_room_entity != None:
            with loading_area:
                with st_lottie_spinner(animation_source=LottieManager.LOADING):
                    chat_messages_manager = ChatMessagesManager.init_as_continue(room_id=selected_room_entity.room_id)
                    ChatMessagesSState.set(value=chat_messages_manager)
                    ComponentSState.set_chat_room_entity()
                    cls.deinit()
                    st.rerun()

    @staticmethod
    def deinit() -> None:
        CreateProcesserSState.deinit()
