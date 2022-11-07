from Transition import Transition


class OkTransition(Transition):
    def __init__(self):
        self.__next_state = None


    @property
    def is_valid(self) -> bool:
        return True

    @property
    def next_state(self):
        return self.__next_state

    @next_state.setter
    def next_state(self, new_state):
        self.__next_state = new_state

    def is_transiting(self) -> bool:
        return True

    def _do_transiting_action(self):
        pass

    def exec_transiting_action(self):
        self._do_transiting_action()
