from abc import ABC, abstractmethod
from queue import Queue, Empty
from threading import Thread
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar


T = TypeVar("T")


class QueueResponse(Generic[T]):
    def __init__(self, content: T, is_finish: bool = False) -> None:
        self._content = content
        self._is_finish = is_finish

    @property
    def content(self) -> T:
        return self._content

    @property
    def is_finish(self) -> bool:
        return self._is_finish

    def __str__(self) -> str:
        return str(self._content)


class QueueHandler(Generic[T]):
    def __init__(self, timeout_sec: float = 1) -> None:
        self._queue = Queue()
        self._timeout_sec = timeout_sec

    def send(self, content: T, is_finish: bool = False) -> None:
        response = QueueResponse[T](content, is_finish)
        self._queue.put(response)

    def receive(self) -> Optional[QueueResponse[T]]:
        try:
            return self._queue.get(timeout=self._timeout_sec)
        except Empty:
            return None


class BaseProcesser(Generic[T], Thread, ABC):
    def __init__(self, timeout_sec: float = 1.0) -> None:
        super().__init__()
        self._queue_handler = QueueHandler[T](timeout_sec)
        self._has_inner_dict = False

    def add_queue(self, content: T, is_finish: bool = False):
        self._queue_handler.send(content=content, is_finish=is_finish)

    def start_and_wait_to_complete(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        self._outer_dict = outer_dict
        if not self._has_inner_dict:
            self._inner_dict = inner_dict
            self._has_inner_dict = True

        self.pre_process(self._outer_dict, self._inner_dict)

        try:
            self.start()
        except RuntimeError:
            pass
        finally:
            while True:
                if not self.is_alive():
                    break
                response = self._queue_handler.receive()
                if response is None:
                    continue
                self.callback_process(response.content, self._outer_dict, self._inner_dict)
                if response.is_finish:
                    break
            self.join()

        self.post_process(self._outer_dict, self._inner_dict)

    def run(self) -> None:
        self.main_process(self._inner_dict)

    @abstractmethod
    def main_process(self, inner_dict: Dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def pre_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def callback_process(self, content: T, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class EarlyStopProcessException(Exception):
    def __init__(self, message="Process stopped earlier than expected"):
        super().__init__(message)


class BaseProcessersManager(ABC):
    def __init__(self, processer_class_list: List[Type[BaseProcesser]]) -> None:
        self._processer_class_list = processer_class_list
        self._is_running = False
        self._inner_dict = {}
        self._outer_dict = {}

    def init_processers(self, without_is_running=False) -> None:
        self._processers = [processer_class() for processer_class in self._processer_class_list]
        self._inner_dict = {}
        self._outer_dict = {}
        if not without_is_running:
            self._is_running = False

    def run_all(self, **kwargs) -> None:
        is_running = self._is_running
        self._is_running = True

        # run pre-process
        if not is_running:
            self.init_processers(without_is_running=True)
            try:
                self._outer_dict, self._inner_dict = self.pre_process_for_starting(**kwargs)
            except EarlyStopProcessException:
                self._is_running = False
                return
        else:
            self._outer_dict = self.pre_process_for_running(**kwargs)

        # run main-processes
        for processer in self._processers:
            processer.start_and_wait_to_complete(self._outer_dict, self._inner_dict)

        # run post-process
        self.post_process(self._outer_dict, self._inner_dict)

        self._is_running = False

    @abstractmethod
    def pre_process_for_starting(self, **kwargs) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def pre_process_for_running(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def post_process(self, outer_dict: Dict[str, Any], inner_dict: Dict[str, Any]) -> None:
        raise NotImplementedError("Subclasses must implement this method")
