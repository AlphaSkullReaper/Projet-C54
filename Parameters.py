from xmlrpc.client import Boolean


class Parameters:
    terminal: Boolean
    do_in_state_when_entering: Boolean = False
    do_in_state_action_when_exiting: Boolean = False