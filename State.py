from formatter import NullFormatter
from symbol import parameters
from Parameters import Parameters as param
from Transition import Transition as trans

class State:
    parameters: param
    transition = [trans]

    def State(param: param):
        parameters = param
    
    def is_Valid():
        valid = False
        for val in transition:
            if(val.is_valid()):
                valid = True
            else:
                valid = False


    def is_Terminal():
        return param.terminal

    def is_Transiting():
        return trans.is_transiting
    
    def add_Transition(next_transition: trans):
        transition.append(next_transition)
    
    def exec_entering_action():
        do_entering_action()
    
    def exec_in_state_action():
        do_in_state_action()
    
    def exec_exiting_action():
        do_exiting_action()