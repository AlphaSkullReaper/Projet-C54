from Transition import Transition
from abc import abstractmethod

class State:
    class Parameters:
        terminal: bool
        do_in_state_when_entering: bool = False
        do_in_state_action_when_exiting: bool = False

    def __init__(self, parameters: 'Parameters' = Parameters()):
        self.__parameters = parameters
        self.__transition: Transition = []

    @property
    def is_valid(self) -> 'bool':
        if len(self.__transition) >= 1:
            for val in self.__transition:
                if not val.is_valid:
                    return False
        return True

    @property
    def is_terminal(self):
        return self.__parameters.terminal

    @property
    def is_transiting(self) -> 'Transition' or None:
        if len(self.__transition) >= 1:
            for val in self.__transition:
                if val.is_transiting:
                    return val
        return None

    def add_transition(self, next_transition: Transition):
        if next_transition is Transition:
            self.__transition.append(next_transition)
        else:
            raise Exception("Error: Expecting a Type Transition!")

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
