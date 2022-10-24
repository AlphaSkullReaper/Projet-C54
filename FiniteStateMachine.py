from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class FiniteStateMachine:

    class OperationalState(Enum):
        UNITIALIZED = 1
        IDLE = 2
        RUNNING = 3
        TERMINAL_REACHED = 4

    def __init__(self, layout_parameter, unitialized:bool = True): #do typing layount:Layount
        self.__layout = layout_parameter
        self.__current_applicative_state = layout_parameter.initial_state
        self.__current_operational_state = OperationalState.UNITIALIZED if unitialized else  OperationalState.IDLE #if non unitialised what set does it start it in?
     
    #expression_if_true if condition else expression_if_false
    @property
    def layout(self):
        return self.__layout

    @layout.setter
    def layout(self,value): #do typing value:Layount
        self.__layout = value


    @property
    def current_applicative_state(self):
        return self.__current_applicative_state

    @current_applicative_state.setter
    def current_applicative_state(self,value): #do typing value:state
        self.__current_applicative_state = value

    @property
    def current_operational_state(self):
        return self.__current_operational_state 

    @current_operational_state.setter
    def current_operational_state(self,value:OperationalState):
        self.__current_operational_state = value

  
    def run(self,reset:bool=True,time_budget:float = None):
        if self.__current_operational_state == OperationalState.UNITIALIZED:
            #TODO itialise  here
            self.__current_operational_state = OperationalState.IDLE
        if  self.__current_operational_state == OperationalState.IDLE or self.__current_operational_state == OperationalState.RUNNING:
            startime = datetime.now()
            endtime = datetime.now()
            while (datetime.timestamp(endtime) - datetime.timestamp(startime)) < time_budget:
                endtime = datetime.now()
                if self.track() == False:
                    break

    def track(self)->bool:
        if self.__current_applicative_state != None and self.__current_applicative_state.is_valid():
            self.__current_operational_state = OperationalState.RUNNING
            if self.__current_applicative_state.is_transiting() != None:
                if (self.__current_applicative_state.is_terminal() ):
                    if self.__current_applicative_state.do_in_action_when_exiting:
                        self.__current_applicative_state.exec_exiting_action()
                    self.__current_operational_state = OperationalState.TERMINAL_REACHED        
                    return False
        
                else:
                    self._transit_by(self.__current_applicative_state.is_transiting())
            else:
                self.__current_applicative_state.exec_in_state_action()
        else:
            self.__current_operational_state = OperationalState.IDLE
        
        
         
    def stop(self):
        pass

    def reset(self):
        pass

    def transit_to(self,state):#force typing state:State
        if self.__current_applicative_state.do_in_action_when_exiting:
            self.__current_applicative_state.exec_exiting_action()
        self.__current_applicative_state = state
        if self.__current_applicative_state.do_in_action_when_entering:
            self.__current_applicative_state.exec_entering_action()
    
  
       

  
    
    def _transit_by(self,transition): #force typing transitation:Transitation
        if self.__current_applicative_state.do_in_action_when_exiting:
            self.__current_applicative_state.exec_exiting_action()
        transition.exec_transiting_action()
        self.__current_applicative_state = transition.nextState
        if self.__current_applicative_state.do_in_action_when_entering:
            self.__current_applicative_state.exec_entering_action()
      

if __name__ == "__main__":
    fine= FiniteStateMachine(1,True)
    fine.run(True,10.0)
   # dt = datetime.now()
    #print(datetime.timestamp(dt))