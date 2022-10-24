from typing import Callable
from State import State
from abc import abstractmethod

class ActionState:
    
    Action = list[Callable[[], None]]
    
    def __init__(self, parameters: State.Parameters = State.Parameters()):
        super().__init__(parameters)
        self.__entering_action: ActionState.Action = []
        self.__in_state_action: ActionState.Action = []
        self.__exiting_actions: ActionState.Action = []
        
    @abstractmethod
    def do_entering_action(self):
        pass
    
    @abstractmethod
    def do_in_state_action(self):
        pass
    
    @abstractmethod
    def do_exiting_action(self):
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