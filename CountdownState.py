from typing import Callable

from FiniteStateMachine import FiniteStateMachine
from OkTransition import OkTransition



class CountdownState(FiniteStateMachine.Layout.State):

    countdown = 0;
    initialcount = 4;

    def __init__(self):
        parameters = FiniteStateMachine.Layout.State.Parameters()
        parameters.do_in_state_when_entering = True
        parameters.do_in_state_action_when_exiting = False
        parameters.terminal = False
        super().__init__(parameters)

    def _do_entering_action(self):
        self.countdown = self.initialcount

    def _do_in_state_action(self):
        self.countdown = self.countdown - 1
        if (self.countdown < 1):
            transition = OkTransition()
            self.add_transition(transition)
        pass

    def _do_exiting_action(self):
        pass

