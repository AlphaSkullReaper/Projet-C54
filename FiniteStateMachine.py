from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional
from State import State
from Transition import Transition
from time import perf_counter


class FiniteStateMachine:
    class OperationalState(Enum):
        UNINITIALIZED = 1
        IDLE = 2
        RUNNING = 3
        TERMINAL_REACHED = 4

    class Layout:
        def __init__(self) -> None:
            self.states = []
            self._initial_state = None

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

        def add_state(self, new_state: 'State') -> None:
            if new_state.is_valid:
                self.states.append(new_state)

        def add_states(self, list_states: list['State']) -> None:
            for a_state in list_states:
                if a_state.is_valid:
                    self.states.append(a_state)

                    #les setters, on veut trap les erreurs le plus vite possible: is instance, raise exeption is false

    def __init__(self, layout_parameter: 'Layout', uninitialized: bool = True) -> None:  # do typing layount:Layount
        self.__layout = layout_parameter
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNINITIALIZED if uninitialized \
            else self.OperationalState.IDLE

    @property
    def current_applicative_state(self) -> 'State':
        return self.__current_applicative_state

    @property
    def current_operational_state(self) -> 'OperationalState':
        return self.__current_operational_state

#Track, si le current state est terminal fais rien.
#3 conditions pour arrêter le while L is etat terminal, quand operational state n'es tpas running, et la troisième si le
    def run(self, reset: bool = True, time_budget: float = None) -> None:
        start_time = perf_counter()
        current_track_state = True
        #reset on stop, reset bool before track,
        if self.__current_operational_state == self.OperationalState.UNINITIALIZED:
            self.__current_applicative_state = self.__layout.initial_state
            self.__current_operational_state = self.OperationalState.IDLE
        if reset:
            self.reset()
        if self.__current_operational_state is not self.OperationalState.TERMINAL_REACHED \
                or self.__current_operational_state is not self.OperationalState.UNINITIALIZED:
            while current_track_state and (time_budget is None or perf_counter() - start_time < time_budget):
                self.__current_operational_state = self.OperationalState.RUNNING
                current_track_state = self.track()
            self.stop()

        #Un pas de simulation de la résolution du state machine.
        #self.__current_operational_state = self.OperationalState.RUNNING

    def track(self) -> bool:
        if self.__current_applicative_state.is_terminal:
            return False

        else:
            transition = self.__current_applicative_state.is_transiting
            if transition is not None:
                self._transit_by(transition)
            else:
                self.__current_applicative_state._exec_in_state_action()
            return True

    def stop(self) -> None:
        self.__current_operational_state = self.OperationalState.IDLE

    def reset(self) -> None:
        self.__current_operational_state = self.OperationalState.IDLE
        self.__current_applicative_state = self.__layout.initial_state  # ON PUISSE REPARTE LA BOUCLE WHILE DE RUN

    def transit_to(self, state: 'State') -> None:
        self.__current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.__current_applicative_state._exec_entering_action()

    def _transit_by(self, transition: 'Transition') -> None:
        self.__current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        self.__current_applicative_state._exec_entering_action()



# dt = datetime.now()
# print(datetime.timestamp(dt))
