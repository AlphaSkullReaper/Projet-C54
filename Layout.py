from typing import Optional
# from State import State


class State:
    def __init__(self):
        pass


class Layout:
    def __init__(self, initial_state: Optional[State] = None, states: Optional[list[State]] = None):
        self.states = states
        self._initial_state = initial_state
        if self.states is None:
            self.states = []
        if self.initial_state is not None:
            self.states.append(self.initial_state)

    def get_validity(self) -> bool:
        validity = False
        if self.states.__contains__(self.initial_state) and isinstance(self.states, list):
            validity = True
        return validity

    @property
    def initial_state(self) -> 'State':
        return self._initial_state

    @initial_state.setter
    def initial_state(self, new_state: State) -> None:
        self._initial_state = new_state
        self.add_state(self._initial_state)

    def add_state(self, new_state: State) -> None:
        self.states.append(new_state)

    def add_states(self, list_states: list[State]) -> None:
        for a_state in list_states:
            self.states.append(a_state)


state = State()
layout = Layout()
print(layout.get_validity())
layout.initial_state = state
print(layout.initial_state)
print(layout.get_validity())
