from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from State import State


class FiniteStateMachine:
    class OperationalState(Enum):
        UNITIALIZED = 1
        IDLE = 2
        RUNNING = 3
        TERMINAL_REACHED = 4

    class Layout:
        def __init__(self, initial_state: Optional['State'] = None, states: Optional[list['State']] = None):
            self.states = states
            self._initial_state = initial_state if initial_state.is_valid else None
            if self.states is None:
                self.states = []
            if self.initial_state is not None:
                self.states.append(self.initial_state)

        @property
        def is_valid(self) -> bool:
            validity = False
            if self.states.__contains__(self.initial_state):
                for a_state in self.states:
                    if a_state is isinstance(self.states, State):
                        validity = True
                    else:
                        validity = False
                        break

            return validity

        @property
        def initial_state(self) -> 'State':
            return self._initial_state

        @initial_state.setter
        def initial_state(self, new_state: 'State') -> None:
            self._initial_state = new_state
            self.add_state(self._initial_state)

        def add_state(self, new_state: 'State') -> None:
            if new_state.is_valid:
                self.states.append(new_state)

        def add_states(self, list_states: list['State']) -> None:
            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)

    def __init__(self, layout_parameter: 'Layout', unitialized: bool = True):  # do typing layount:Layount
        self.__layout = layout_parameter
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNITIALIZED if unitialized \
            else self.OperationalState.IDLE

    @property
    def current_applicative_state(self):
        return self.__current_applicative_state

    @current_applicative_state.setter
    def current_applicative_state(self, value: 'State'):  # do typing value:state
        self.__current_applicative_state = value

    @property
    def current_operational_state(self):
        return self.__current_operational_state

    @current_operational_state.setter
    def current_operational_state(self, value: 'OperationalState'):
        self.__current_operational_state = value

    # TODO: do timer if float isnt none
    #TODO: for loop state in layout state list
    def run(self, reset: bool = True, time_budget: float = None):
        on_continue = True
        if self.__current_operational_state == self.OperationalState.UNITIALIZED:
            self.current_applicative_state = self.__layout.initial_state
            self.current_operational_state = self.OperationalState.IDLE
        while self.__current_operational_state is not self.OperationalState.UNITIALIZED and on_continue:
            on_continue = self.track()

    def track(self) -> bool:
        on_continue = True
        self.__current_operational_state = self.OperationalState.RUNNING
        if self.__current_applicative_state.is_transiting() is not None:
            if self.__current_applicative_state.is_terminal():
                if self.__current_applicative_state.do_in_action_when_exiting:
                    self.__current_applicative_state.exec_exiting_action()
                else:
                    self.__current_applicative_state.exec_in_state_action()
                self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
                on_continue = False


            else:
                self._transit_by(self.__current_applicative_state.is_transiting())

        else:
            self.__current_applicative_state.exec_in_state_action()
        return on_continue

    def stop(self):
       self.current_operational_state = self.OperationalState.UNITIALIZED

    def reset(self):
        self.current_operational_state = self.OperationalState.IDLE
        self.current_applicative_state = self.__layout.initial_state

    def transit_to(self, state: 'State'):
        if self.__current_applicative_state.do_in_action_when_exiting:
            self.__current_applicative_state.exec_exiting_action()
        self.__current_applicative_state = state
        if self.__current_applicative_state.do_in_action_when_entering:
            self.__current_applicative_state.exec_entering_action()

    def _transit_by(self, transition: 'Transition'):
        if self.__current_applicative_state.do_in_action_when_exiting:
            self.__current_applicative_state.exec_exiting_action()
        transition.exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        if self.__current_applicative_state.do_in_action_when_entering:
            self.__current_applicative_state.exec_entering_action()


if __name__ == "__main__":
    initialState = State()
    layout = FiniteStateMachine.Layout(initialState)
# dt = datetime.now()
# print(datetime.timestamp(dt))
