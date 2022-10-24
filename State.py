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
        total_valid = 0
        if self.__transition.len() >= 1:
            for val in self.__transition:
                if val.is_transiting:
                    total_valid += 1
            if total_valid == self.__transition.len():
                valid = True
        
        return valid

    @property
    def is_terminal(self):
        return self.__parameters.terminal

    @property
    def is_transiting(self):
        valid = False
        i = 0
        while valid == False:
            if self.__transition[i].is_transiting:
                valid = True
            i += 1
            
        return valid

    def add_transition(self, next_transition: trans):
        if next_transition is trans:
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
