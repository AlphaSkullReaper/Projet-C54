from typing import Callable
from abc import abstractmethod
from FiniteStateMachine import FiniteStateMachine

class ActionState(FiniteStateMachine.Layout.State):
    
    Action = Callable[[], None]
    
    def __init__(self, parameters: 'FiniteStateMachine.Layout.State.Parameters' = FiniteStateMachine.Layout.State.Parameters()):
        super().__init__(parameters)
        self.__entering_action: ActionState.Action = []
        self.__in_state_action: ActionState.Action = []
        self.__exiting_actions: ActionState.Action = []
    
    @abstractmethod
    def _do_entering_action(self):
        pass
    
    @abstractmethod
    def _do_in_state_action(self):
        pass
    
    @abstractmethod
    def _do_exiting_action(self):
        pass
    
    def add_entering_action(self, action: Action):
        if action is ActionState.Action:
            self.__entering_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")
        
    def add_in_state_action(self, action: Action):
        if action is ActionState.Action:
            self.__in_state_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")
    
    def add_exiting_action(self, action: Action):
        if action is ActionState.Action:
            self.__exiting_actions.append(action)
        else:
            raise Exception("Error: Expecting Type Action")