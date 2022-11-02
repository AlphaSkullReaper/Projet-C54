from typing import Callable
from abc import abstractmethod
from State import State

<<<<<<< HEAD
class ActionState(State):
=======

class ActionState(FiniteStateMachine.Layout.State):
>>>>>>> 6bb8b40248eaa312375c03eb1fe597e0ece1638d
    
    Action = Callable[[], None]
    
    def __init__(self, parameters: 'State.Parameters' = State.Parameters()):
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