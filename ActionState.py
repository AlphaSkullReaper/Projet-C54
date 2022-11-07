from typing import Callable
from abc import abstractmethod
from State import State


class ActionState(State):
    Action = Callable[[], None]

    def __init__(self, parameters: 'State.Parameters' = State.Parameters()) -> None:
        super().__init__(parameters)
        self.__entering_action: list[ActionState.Action] = []
        self.__in_state_action: list[ActionState.Action] = []
        self.__exiting_actions: list[ActionState.Action] = []

    @abstractmethod
    def _do_entering_action(self) -> None:
        pass

    @abstractmethod
    def _do_in_state_action(self) -> None:
        pass

    @abstractmethod
    def _do_exiting_action(self) -> None:
        pass

    def add_entering_action(self, action: 'Action') -> None:
        if action is ActionState.Action:
            self.__entering_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")

    def add_in_state_action(self, action: 'Action') -> None:
        if action is ActionState.Action:
            self.__in_state_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")

    def add_exiting_action(self, action: 'Action') -> None:
        if action is ActionState.Action:
            self.__exiting_actions.append(action)
        else:
            raise Exception("Error: Expecting Type Action")
