from streamlit.delta_generator import DeltaGenerator

from model import ChatRoomEntity


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
    def title(self) -> str:
        return self._title

    @property
    def message_area(self) -> DeltaGenerator:
        return self._message_area

    @property
    def loading_area(self) -> DeltaGenerator:
        return self._loading_area

    @property
    def is_pushed(self) -> bool:
        return self._is_pushed


class RoomContainerActionResults:
    def __init__(
        self,
        is_pushed: bool,
        loading_area: DeltaGenerator,
    ) -> None:
        self._is_pushed = is_pushed
        self._loading_area = loading_area

    @property
    def is_pushed(self) -> bool:
        return self._is_pushed

    @property
    def loading_area(self) -> DeltaGenerator:
        return self._loading_area


class EnterActionResults:
    def __init__(
        self,
        chat_room_entity: ChatRoomEntity,
        loading_area: DeltaGenerator,
    ) -> None:
        self._chat_room_entity = chat_room_entity
        self._loading_area = loading_area

    @property
    def chat_room_entity(self) -> ChatRoomEntity:
        return self._chat_room_entity

    @property
    def loading_area(self) -> DeltaGenerator:
        return self._loading_area