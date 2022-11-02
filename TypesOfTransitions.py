from re import A
from tkinter.messagebox import NO
from typing import Callable
from transition import Transition
import time
from State import State
from Condition import *

"""
           ______________________________________
  ________|                                      |_______
  \       |         CONDITIONALTRANSITION        |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
class ConditionalTransition(Transition):
    def __init__(self, condition: 'Condition' = None, next_state: 'State' = None):
        super().__init__(next_state)
        if isinstance(condition, 'Condition'):
            self.__condition = condition

    @property
    def is_valid(self) -> bool:
        return self.__condition and self.__next_state is not None
    
    @property 
    def condition(self) -> 'Condition':
        return self.__condition

    @condition.setter
    def condition(self, new_condition) -> 'Condition':
        self.__condition = new_condition

    # chaque objet a une valeur bool, en overridant __bool__, on détermine quand condition est valide
    # https://docs.python.org/3/reference/datamodel.html?highlight=__bool__#object.__bool__ 
    def is_transiting(self) -> bool:
        return bool(self.__condition) 


"""
           ______________________________________
  ________|                                      |_______
  \       |           ACTIONTRANSITION           |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
class ActionTransition(ConditionalTransition):
    Action = Callable[[], None]

    def __init__(self, next_state: 'State' = None):
        super().__init__(next_state)
        self.__transiting_actions:  list[ActionTransition.Action] = []
 
    def _do_transiting_action(self):
        for action in self.__transiting_actions:
            action()

    def add_transiting_action(self, action: 'Action'):
        if isinstance(action, 'Action'):
            self.__transiting_actions.append(action)
        else:
            raise Exception("ERROR: Invalid Transiting Action")


"""
           ______________________________________
  ________|                                      |_______
  \       |          MONITOREDTRANSITION         |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
class MonitoredTransition(ActionTransition):
    def __init__(self, next_state: 'State' = None):
        super().__init__(next_state) 
        self.__transit_count: int = 0
        self.__last_transit_time: float = 0
        self.custom_value: any = None
        
    @property
    def transit_count(self) -> int:
        return self.__transit_count
    
    @property
    def last_transit_time(self) -> int:
        return self.__last_transit_time
    
    def reset_transit_count(self):
        self.__transit_count = 0
        
    def reset_last_transit_time(self):
        self.__last_transit_time = 0
        
    def _exec_transiting_action(self):
        self.__last_transit_time = time.perf_counter()
        self.__transit_count += 1

        super()._exec_transiting_action()