from abc import abstractmethod
from curses.ascii import NUL
import time

"""
           ______________________________________
  ________|                                      |_______
  \       |             CONDITION                |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
class Condition:
    def __init__(self, inverse: bool = False):
        self.__inverse = inverse

    @abstractmethod
    def _compare(self) -> bool:
        pass
    
    # https://docs.python.org/3/reference/datamodel.html?highlight=__bool__#object.__bool__
    def __bool__(self) -> bool:
        return self._compare ^ self.__inverse
        #return not self._compare() if self.__inverse else self._compare()


"""
           ______________________________________
  ________|                                      |_______
  \       |         ALWAYSTRUECONDITION          |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
class AlwaysTrueCondition(Condition):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
       return True


"""
           ______________________________________
  ________|                                      |_______
  \       |            VALUECONDITION            |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
class ValueCondition(Condition):
    def __init__(self,initial_value: any, expected_value:any, inverse: bool = False):
        super().__init__(inverse)
        self.expected_value: any = expected_value
        self.value: any = initial_value

    def _compare(self) -> bool:
       return True if self.value == self.expected_value else False


"""
           ______________________________________
  ________|                                      |_______
  \       |           TIMEDCONDITION             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\  
"""
class TimedCondition(Condition):
    def __init__(self,duration: float = 1., time_reference:float = None, inverse: bool = False):
        super().__init__(inverse)
        self.__counter_duration: float = duration
        if time_reference is None:
            self.__counter_reference = time.perf_counter()
        else:
            self.__counter_reference = time_reference
        

    def _compare(self) -> bool:
        
        return time.perf_counter() - self.__counter_reference >= self.__counter_duration

    @property
    def duration(self) -> float:
        return self.__counter_duration

    @duration.setter
    def duration(self, new_duration: float) -> float:
        self.__counter_duration = new_duration
    
    def reset(self):
        pass

"""
           ______________________________________
  ________|                                      |_______
  \       |           MANYCONDITIONS             |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""

"""     
----------------8<-------------[ ManyConditions ]--------------- 
"""
class ManyConditions(Condition):

    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        self._conditions: 'Condition' = []

    def add_condition(self, condition: 'Condition'):
        self._conditions.append(condition)

    def add_conditions(self, conditionList: list['Condition']):
        self._conditions.extend(conditionList)


"""     
----------------8<-------------[ AllConditions ]----------------- 
"""
class AllConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
    
    def _compare(self) -> bool:
        pass


"""     
----------------8<-------------[ AnyConditions ]----------------- 
"""
class AnyConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        pass


"""     
----------------8<-------------[ NoneConditions ]---------------- 
"""
class NoneConditions(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self) -> bool:
        pass



"""
           ______________________________________
  ________|                                      |_______
  \       |        MONITOREDSTATECONDITION       |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""
class MonitoredStateCondition(Condition):
    def __init__(self, monitered_state: 'MonitoredState', inverse: bool = False):
        if isinstance(monitered_state, 'MonitoredState'):
            super().__init__(inverse)
            self._monitered_state = monitered_state
    
    @property
    def monitered_state(self) -> 'MonitoredState':
        return self._monitered_state
    
    @monitered_state.setter
    def monitered_state(self, monitered_state: 'MonitoredState'):
        self._monitered_state = monitered_state


"""     
----------------8<-------------[ StateEntryDurationCondition ]------ 
"""
class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration: float, monitered_state: 'MonitoredState', inverse: bool = False):
        super().__init__(monitered_state, inverse)
        self.__duration = duration

    def _compare(self) -> bool:
        pass

    @property
    def duration(self) -> float: 
        return self._duration

    @duration.setter
    def duration(self, new_duration):
        self._duration = new_duration

    


"""     
----------------8<-------------[ StateEntryCountCondition ]--------- 
"""
class StateEntryCountCondition(MonitoredStateCondition):
    def __init__(self, expected_count: int, monitered_state: 'State', auto_reset:bool = False, inverse: bool = False):
        super().__init__(monitered_state, inverse)
        self.__auto_reset = auto_reset
        self.__expected_count = expected_count

    def _compare(self) -> bool:
        pass
        #compare if ref_count == expected_count?

    def reset_count(self):
        pass
    
    @property
    def expected_count(self) -> int:
        return self._expected_count

    @expected_count.setter
    def expected_count(self, new_expected_count):
        self.__expected_count = new_expected_count
     


"""     
----------------8<-------------[ StateValueCondition ]------------- 
"""
class StateValueCondition(MonitoredStateCondition):
    def __init__(self, expected_value: any, monitered_state: 'State', inverse: bool = False):
        super().__init__(monitered_state, inverse)
        self.__expected_value = expected_value
    
    def _compare(self) -> bool:
        pass

    @property
    def expected_value(self) -> any:
        return self._expected_value

    @expected_value.setter
    def expected_value(self, new_expected_value: any):
        self.__expected_value = new_expected_value
    
