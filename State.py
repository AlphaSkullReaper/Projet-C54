from Transition import Transition as trans
from abc import abstractmethod


class State:
    class Parameters:
        terminal: bool
        do_in_state_when_entering: bool = False
        do_in_state_action_when_exiting: bool = False

    def __init__(self, param: 'Parameters' = Parameters()):
        self.__parameters = param
        self.__transition = [trans]

    @property
    def is_valid(self) -> bool:
        valid = False
        for val in self.__transition:
            if val.is_valid():
                valid = True
            else:
                valid = False

        return valid

    @property
    def is_Terminal(self):
        return self.__parameters.terminal

    @property
    def is_Transiting(self):
        return self.__transition.is_transiting

    def add_Transition(self, next_transition: trans):
        self.__transition.append(next_transition)

    @abstractmethod
    def _do_entering_action(self):
        pass

    @abstractmethod
    def _do_in_state_action(self):
        pass

    @abstractmethod
    def _do_exiting_action(self):
        pass

    @abstractmethod
    def _exec_entering_action(self):
        self._do_entering_action()

    @abstractmethod
    def _exec_in_state_action(self):
        self._do_in_state_action()

    @abstractmethod
    def _exec_exiting_action(self):
        self._do_exiting_action()
