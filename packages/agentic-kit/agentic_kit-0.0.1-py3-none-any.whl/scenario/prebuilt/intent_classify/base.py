def intent_retry_failed_callback(retry_state):
    """return the result of the last call attempt"""
    print('---intent_retry_failed_callback: %s' % retry_state)
    return { 'intent': '', 'intent_keywords': [], 'should_finish': True }
