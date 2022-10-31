from CountdownState import CountdownState
from FiniteStateMachine import FiniteStateMachine

if __name__ == "__main__":
    initialState = CountdownState()
    layout = FiniteStateMachine.Layout(initialState)
    fsm = FiniteStateMachine(layout)
    newstate = CountdownState()
    layout.add_state(newstate)
    newstate2 = CountdownState()
    layout.add_state(newstate2)
    fsm.run()


