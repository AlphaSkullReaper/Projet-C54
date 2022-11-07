from abc import abstractmethod
from Transition import Transition


class State:
    class Parameters:
        terminal: bool
        do_in_state_when_entering: bool = False
        do_in_state_action_when_exiting: bool = False

    def __init__(self, parameters: 'Parameters' = Parameters()) -> None:
        self.__parameters = parameters
        self.__transition: list['Transition'] = []

    @property
    def is_valid(self) -> 'bool':
        if len(self.__transition) >= 1:
            for val in self.__transition:
                if not val.is_valid:
                    return False
        return True

    @property
    def is_terminal(self) -> bool:
        return self.__parameters.terminal

    @property
    def is_transiting(self) -> 'Transition' or None:
        if len(self.__transition) >= 1:
            for val in self.__transition:
                if val.is_transiting:
                    return val
        else:
            return None

    def add_transition(self, next_transition: 'Transition') -> None:
        if next_transition is Transition:
            self.__transition.append(next_transition)
        else:
            raise Exception("Error: Expecting a Type Transition!")

    @abstractmethod
    def _do_entering_action(self) -> None:
        pass

    @abstractmethod
    def _do_in_state_action(self) -> None:
        pass

    @abstractmethod
    def _do_exiting_action(self) -> None:
        pass

    @abstractmethod
    def _exec_entering_action(self) -> None:
        self._do_entering_action()

    @abstractmethod
    def _exec_in_state_action(self) -> None:
        self._do_in_state_action()

    @abstractmethod
    def _exec_exiting_action(self) -> None:
        self._do_exiting_action()
