import niveau1
from niveau1 import FiniteStateMachine, State, Transition, TestingState
from niveau2 import AlwaysTrueCondition, ConditionalTransition, ActionState, MonitoredState, ActionTransition, \
    MonitoredTransition

"""
           ______________________________________
  ________|                                      |_______
  \       |         ALWAYSTRUECONDITION          |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 
"""
"""
condition_always = AlwaysTrueCondition()

p1 = State.Parameters(False, True, False)
state1 = ActionState(p1)
state1.add_entering_action(lambda: print("Ta mère en froc"))
state1.add_exiting_action(lambda: print("Ton père en jaquette"))

p2 = State.Parameters(False, True, False)
state2 = ActionState(p2)
state2.add_entering_action(lambda: print("Ta soeur en crocs"))
state2.add_exiting_action(lambda: print("Ton frère en flanellette"))

p3 = State.Parameters(True, True, False)
state3 = ActionState(p3)
state3.add_exiting_action(lambda: print("Famille de tous nus"))

transition_conditional = ConditionalTransition(condition_always, state2)
transition_conditional2 = ConditionalTransition(condition_always, state3)
transition_conditional3 = ConditionalTransition(condition_always, state1)

state1.add_transition(transition_conditional)
state2.add_transition(transition_conditional2)
state3.add_transition(transition_conditional3)

layout = FiniteStateMachine.Layout()
layout.add_states([state1,state2, state3])
layout.initial_state = state1

MyStateMachine = FiniteStateMachine(layout)

MyStateMachine.run(False)
"""

"""
           ______________________________________
  ________|                                      |_______
  \       |            MONITOREDSTATE            |      /
   \      |                                      |     /
   /      |______________________________________|     \ 
  /__________)                                (_________\ 

"""
""""
condition_always = AlwaysTrueCondition()


p1 = State.Parameters(False, True, False)
state1 = MonitoredState(p1)
state1.add_entering_action(lambda: print("entrycount state 1",state1.entry_count))
state1.add_exiting_action(lambda: print("exit time state 1",state1.last_exit_time))

p2 = State.Parameters(False, True, False)
state2 = MonitoredState(p2)
state2.add_entering_action(lambda: print("entrycount state 2",state2.entry_count))
state2.add_exiting_action(lambda: print("exit time state 2",state2.last_exit_time))

p3 = State.Parameters(True, True, False)
state3 = MonitoredState(p3)
state3.add_entering_action(lambda: print("entrycount state 3",state3.entry_count))
state3.add_exiting_action(lambda: print("exit time state 3",state3.entry_count))

transition_conditional = ConditionalTransition(condition_always, state2)
transition_conditional2 = ConditionalTransition(condition_always, state3)
transition_conditional3 = ConditionalTransition(condition_always, state1)

state1.add_transition(transition_conditional)
state2.add_transition(transition_conditional2)
state3.add_transition(transition_conditional3)

layout = FiniteStateMachine.Layout()
layout.add_states([state1,state2, state3])
layout.initial_state = state1

MyStateMachine = FiniteStateMachine(layout)

MyStateMachine.run(False)
"""
""""
condition_always = AlwaysTrueCondition()


p1 = State.Parameters(False, True, False)
state1 = MonitoredState(p1)
state1.add_entering_action(lambda: print("entrycount state 1",state1.entry_count))
state1.add_exiting_action(lambda: print("exit time state 1",state1.last_exit_time))

p2 = State.Parameters(False, True, False)
state2 = MonitoredState(p2)
state2.add_entering_action(lambda: print("entrycount state 2",state2.entry_count))
state2.add_exiting_action(lambda: print("exit time state 2",state2.last_exit_time))

p3 = State.Parameters(True, True, False)
state3 = MonitoredState(p3)
state3.add_entering_action(lambda: print("entrycount state 3",state3.entry_count))
state3.add_exiting_action(lambda: print("exit time state 3",state3.entry_count))

transition_action1 = ActionTransition(condition_always, state2)
transition_action1.add_transiting_action(lambda : print("transiting 1"))
transition_action2 = ActionTransition(condition_always, state3)
transition_action1.add_transiting_action(lambda : print("transiting 2"))
transition_action3 = ActionTransition(condition_always, state1)
transition_action1.add_transiting_action(lambda : print("transiting 3"))

state1.add_transition(transition_action1)
state2.add_transition(transition_action2)
state3.add_transition(transition_action3)

layout = FiniteStateMachine.Layout()
layout.add_states([state1,state2, state3])
layout.initial_state = state1

MyStateMachine = FiniteStateMachine(layout)

MyStateMachine.run(False)
"""
condition_always = AlwaysTrueCondition()


p1 = State.Parameters(False, True, False)
state1 = MonitoredState(p1)
state1.add_entering_action(lambda: print("entrycount state 1",state1.entry_count))
state1.add_exiting_action(lambda: print("exit time state 1",state1.last_exit_time))

p2 = State.Parameters(False, True, False)
state2 = MonitoredState(p2)
state2.add_entering_action(lambda: print("entrycount state 2",state2.entry_count))
state2.add_exiting_action(lambda: print("exit time state 2",state2.last_exit_time))

p3 = State.Parameters(False, True, False)
state3 = MonitoredState(p3)
state3.add_entering_action(lambda: print("entrycount state 3",state3.entry_count))
state3.add_exiting_action(lambda: print("exit time state 3",state3.entry_count))

transition_action1 = MonitoredTransition(condition_always, state2)
transition_action1.add_transiting_action(lambda : print("transiting 1",transition_action1.transit_count))
transition_action2 = MonitoredTransition(condition_always, state3)
transition_action1.add_transiting_action(lambda : print("transiting 2",transition_action2.transit_count))
transition_action3 = MonitoredTransition(condition_always, state1)
transition_action1.add_transiting_action(lambda : print("transiting 3",transition_action3.transit_count))

state1.add_transition(transition_action1)
state2.add_transition(transition_action2)
state3.add_transition(transition_action3)

layout = FiniteStateMachine.Layout()
layout.add_states([state1,state2, state3])
layout.initial_state = state1

MyStateMachine = FiniteStateMachine(layout)

MyStateMachine.run(False)

if __name__ == '__main__':
    print("DON'T MIND IF I DO!")
