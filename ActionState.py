from State import State
from abc import abstractmethod

class ActionState:
    
    class Action:
        pass
    
    def __init__(self, parameters: State.Parameters()):
        State.__init__(parameters)
        self.__entering_action = [Action]
        self.__in_state_action = [Action]
        self.__exiting_actions = [Action]
        
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
        if action is Action:
            self.__entering_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")
        
    def add_in_state_action(self, action: Action):
        if action is Action:
            self.__in_state_action.append(action)
        else:
            raise Exception("Error: Expecting Type Action")
    
    def add_exiting_action(self, action: Action):
        if action is Action:
            self.__exiting_actions.append(action)
        else:
            raise Exception("Error: Expecting Type Action")