
def transition(current_state, allowed_states, next_state, state_change, on_success=None, on_failure=None):
    if not current_state in allowed_states:
        if on_failure: on_failure()
        return False

    state_change(next_state)
    if on_success: on_success()
    return True
