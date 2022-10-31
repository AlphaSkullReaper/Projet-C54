from typing import Optional
from State import State


# Infrastructure de l'état et des transitions que l'on doit résoudre;
# Inner lasse de FiniteStateMachine, publique
# L'intention derrière le design est de passer à Dinite State Machine un layout


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


state = State()
layout = Layout(state)
print(layout.is_valid())
layout.initial_state = state
print(layout.initial_state)
print(layout.is_valid())
