from abc import ABC, abstractmethod

from typing import Union


class Transition(ABC):
    def __init__(self, next_state: 'State' = None):
        if isinstance(next_state,'State'):
            self.__next_state = next_state
        else:
            raise Exception("ERROR STATE NOT VALID")

    @property
    def is_valid(self) -> bool:
        return self.__next_state is not None

    @property
    def next_state(self):
        return self.__next_state

    @next_state.setter
    def next_state(self, new_state):
        self.__next_state = new_state

    @abstractmethod
    def is_transiting(self) -> bool:
        pass

    def _do_transiting_action(self):
        pass

    def _exec_transiting_action(self):
        self._do_transiting_action()
