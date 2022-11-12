import niveau1
from niveau1 import FiniteStateMachine, State, Transition, TestingState
from niveau2 import AlwaysTrueCondition, ConditionalTransition, ActionState

condition_always = AlwaysTrueCondition()

# parameters1 = ActionState.Parameters()
# parameters1.do_in_state_action_when_exiting = True
# parameters1.do_in_state_when_entering = True
#
# parameters2 = ActionState.Parameters()
# parameters2.do_in_state_action_when_exiting = True
# parameters2.do_in_state_when_entering = True
#
# parameters3 = ActionState.Parameters()
# parameters3.terminal = True
# parameters3.do_in_state_action_when_exiting = True

state1 = ActionState()
state1.Parameters.do_in_state_when_entering = True
#state1.Parameters.terminal = True

state1.add_entering_action(lambda: print("Ta mère en froc"))
state1.add_exiting_action(lambda: print("Ton père en jaquette"))


state2 = ActionState()
state2.Parameters.do_in_state_when_entering = True
state2.add_entering_action(lambda: print("Ta soeur en crocs"))
state2.add_exiting_action(lambda: print("Ton frère en flanellette"))

state3 = ActionState()
state3.Parameters.do_in_state_action_when_exiting = True
state3.add_exiting_action(lambda: print("Famille de tous nus"))
#state3.Parameters.terminal = True

transition_conditional = ConditionalTransition(condition_always, state2)
transition_conditional2 = ConditionalTransition(condition_always, state3)
transition_conditional3 = ConditionalTransition(condition_always, state1)

state1.add_transition(transition_conditional)
state2.add_transition(transition_conditional2)
state3.add_transition(transition_conditional3)


layout = FiniteStateMachine.Layout()
layout.initial_state = state1
layout.add_states([state2, state3])

MyStateMachine = FiniteStateMachine(layout)

MyStateMachine.run()

if __name__ == '__main__':
    print(state1.Parameters)
